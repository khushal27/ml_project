from housing.entity.config_entity import DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from housing.exception import HousingException
from housing.logger import logging
from housing.utils.utils import read_yaml
import os,sys
import pandas as pd
from housing.constant import *

class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig
                ,data_ingestion_artifact:DataIngestionArtifact
                ,data_validation_artifact:DataValidationArtifact):
        try:
            logging.info(f"{'>>'*20}Data Tranformation log started.{'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact:data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_numerical_columns(self,X):
        try:
            self.numerical_columns_list = [col for col,colType in X.dtypes.iteritems() if colType != 'O']
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_categorical_columns(self,X):
        try:
            self.categorical_columns_list = [col for col,colType in X.dtypes.iteritems() if colType == 'O']
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def get_null_numerical_columns(self,X):
        try:
            self.numerical_columns_list = [col for col,colType in X.dtypes.iteritems() if colType != 'O' and X[col].isna().sum() > 0]
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_null_categorical_columns(self,X):
        try:
            self.null_categorical_columns_list = [col for col,colType in X.dtypes.iteritems() if colType == 'O' and X[col].isna().sum() > 0]
        except Exception as e:
            raise HousingException(e,sys) from e

    def check_and_fill_missing_values(self):
        try:
            train_data = self.data_ingestion_artifact.train_file
            X = pd.read_csv(train_data)
            self.get_null_numerical_columns(X)
            #print(self.numerical_columns_list)
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def one_hot_encoding(self):
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e

    #@staticmethod
    def load_data(file_path:str,schema_file_path:str)->pd.DataFrame:
        try:
            dataset_schema = read_yaml(schema_file_path)
            
            dataframe = pd.read_csv(file_path)

            schema = dataset_schema[DATA_SET_SCHEMA_COLUMNS_KEY]
            error_msg = ""
            for col in dataframe.columns:
                if col in list(schema.keys()):
                    dataframe[col].astype(schema[col])
                else:
                    error_msg = f"{error_msg} \nColumns: [{col}] is not in the schema file"
            if len(error_msg) > 0:
                raise Exception(error_msg)
            return dataframe
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def initiate_data_transformation(self):
        try:
            self.check_and_fill_missing_values()
        except Exception as e:
            raise HousingException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20}Data Transformation log Completed.{'<<'*20}")