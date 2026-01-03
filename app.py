from flask import Flask,render_template,request
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
from src.logger import logging
from src.exception import CustomException
import sys

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    try:
        if request.method=='GET':
            return render_template('home.html')
        else:
            form_data=CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score'))
            )
            logging.info("Collecting form data to dataframe")
            form_df=form_data.get_data_as_dataframe()
            
            pred_pipeline=PredictPipeline()
            results=pred_pipeline.predict(form_df)
            logging.info("Prediction successful")
            return render_template('home.html', results=results[0])
    except Exception as e:
        logging.error("Error occurred during prediction")
        raise CustomException(e,sys)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)