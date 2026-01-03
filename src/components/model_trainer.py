import sys
import os
from src.logger import logging
from src.exception import CustomException   
from src.utils import save_object, evaluate_models

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
# from catboost import CatBoostRegressor

from dataclasses import dataclass

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    def initiate_model_trainer(self, train_array, test_array):
        try:
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1], 
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )
            models={
                "LinearRegression":LinearRegression(),
                "SVR":SVR(),
                "KNeighborsRegressor":KNeighborsRegressor(),
                "DecisionTreeRegressor":DecisionTreeRegressor(),
                "RandomForestRegressor":RandomForestRegressor(),
                "XGBRegressor":XGBRegressor(),
                # "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "Gradient Boosting": GradientBoostingRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            params={
                "DecisionTreeRegressor": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'splitter':['best','random'],
                    'max_features':['sqrt','log2'],
                },
                "RandomForestRegressor":{
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    'criterion':['squared_error', 'friedman_mse'],
                    'max_features':['sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "LinearRegression":{},
                "SVR":{
                    'kernel':['linear','poly','rbf','sigmoid'],
                    'C':[0.1,0.5,1,5,10],
                },
                "KNeighborsRegressor":{
                    'n_neighbors':[3,5,7,9],
                    'weights':['uniform','distance'],
                    'algorithm':['auto','ball_tree','kd_tree']
                },
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                # "CatBoosting Regressor":{
                #     'depth': [6,8,10],
                #     'learning_rate': [0.01, 0.05, 0.1],
                #     'iterations': [30, 50, 100]
                # },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            logging.info("Starting model evaluation")   
            model_report:dict=evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                              models=models, params=params)
            
            best_model_score = max(sorted(model_report.values()))## highest r2 score
            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]## get the name of best model
            print(f"Keys in models: {models.keys()}")
            print(f"Value in best_model_name: {best_model_name}")
            best_model=models[best_model_name] ## get the best real trained model object
            
            if best_model_score < 0.6:
                logging.info("No best model found")
                raise CustomException("No best model found", sys)
            logging.info(f"Best model found on both training and testing dataset")
            
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=best_model)
            logging.info("Best model is saved")
            
            predicted=best_model.predict(X_test)
            r2_score_value=r2_score(y_test, predicted)
            return(
                r2_score_value,
                best_model_name
            )
        except Exception as e:
            raise CustomException(e,sys)
