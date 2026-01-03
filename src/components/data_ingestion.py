## reading data from various sources
import os
import sys
from src.components import model_trainer
from src.logger import logging
from src.exception import CustomException
from src.components.data_transfromation import DataTransformation
from src.utils import save_object
from src.components.data_transfromation import DataTransformationConfig
from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')
    source_data_path: str = os.path.join('notebook', 'data', 'stud.csv')
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    def intiate_data_ingestion(self):
        logging.info("Entered the data ingestion method")
        try:
            df=pd.read_csv(self.ingestion_config.source_data_path)
            logging.info("Read the dataset as dataframe")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)## create the artifacts folder if not present
            
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw data is saved")
            
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Ingestion of the data is completed")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.info("Exception occurred in the data ingestion method")
            raise CustomException(e, sys)
        
if __name__=="__main__":
    obj = DataIngestion()
    train_path,test_path=obj.intiate_data_ingestion()
    
    data_transformation=DataTransformation()
    train_arr,test_arr,preprocessor_path=data_transformation.intiate_data_tranformation(train_path,test_path)
    
    modeltrainer=ModelTrainer()
    best_r2_score,best_model_name=modeltrainer.initiate_model_trainer(train_arr,test_arr)
    print(f"Best model found , Model name : {best_model_name} , R2 score : {best_r2_score}")
              