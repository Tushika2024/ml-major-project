from flask import Flask,render_template,request,jsonify
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
from src.logger import logging
from src.exception import CustomException
import sys
from flask_cors import CORS

application = Flask(__name__)
app=application  # for AWS deployment
CORS(app)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    try:
        if request.method=='GET':
            return render_template('home.html')
        else:
            data = request.get_json()
            print(f"Received data: {data}")
            form_data=CustomData(
                gender=data.get('gender'),
                race_ethnicity=data.get('ethnicity'),
                parental_level_of_education=data.get('parental_level_of_education'),
                lunch=data.get('lunch'),
                test_preparation_course=data.get('test_preparation_course'),
                reading_score=float(data.get('reading_score')),
                writing_score=float(data.get('writing_score'))
            )
            
            # form_data=CustomData(
            #     gender=request.form.get('gender'),
            #     race_ethnicity=request.form.get('ethnicity'),
            #     parental_level_of_education=request.form.get('parental_level_of_education'),
            #     lunch=request.form.get('lunch'),
            #     test_preparation_course=request.form.get('test_preparation_course'),
            #     reading_score=float(request.form.get('reading_score')),
            #     writing_score=float(request.form.get('writing_score'))
            # )
            logging.info("Collecting form data to dataframe")
            form_df=form_data.get_data_as_dataframe()
            # print(form_df.head())
            
            pred_pipeline=PredictPipeline()
            results=pred_pipeline.predict(form_df)
            logging.info("Prediction successful")
            # return render_template('home.html', results=results[0])
            return jsonify({
            "status": "success",
            "message": f"Processing complete!",
            "result": results[0]
        })
    except Exception as e:
        logging.error("Error occurred during prediction")
        raise CustomException(e,sys)

if __name__ == "__main__":
    app.run(host="0.0.0.0")