from housing.entity.config_entity import DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from housing.exception import HousingException
from housing.logger import logging
from housing.utils.utils import read_yaml,save_array_data, save_object_as_pkl
import os,sys
import pandas as pd
import numpy as np
from housing.constant import *
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

class FeatureGenerator():
    """
    This function generates few columns based on input given

    """
    def __init__(self,add_bedroom_per_room:bool=True,
                total_room_ix = 3,
                population_ix = 5,
                households_ix = 6,
                total_bedrooms_ix = 4,
                columns=None):
        try:
            self.columns = columns
            if self.columns is not None:
                total_room_ix = self.columns.index(DATA_SET_SCHEMA_TOTAL_ROOMS_KEY)
                population_ix = self.columns.index(DATA_SET_SCHEMA_POPULATION_KEY)
                households_ix = self.columns.index(DATA_SET_SCHEMA_HOUSEHOLDS_KEY)
                total_bedrooms_ix = self.columns.index(DATA_SET_SCHEMA_TOTAL_BEDROOM_KEY)

            self.add_bedroom_per_room = add_bedroom_per_room
            self.total_room_ix = total_room_ix
            self.population_ix = population_ix
            self.households_ix = households_ix
            self.total_bedrooms_ix = total_bedrooms_ix
        except Exception as e:
            raise HousingException(e,sys) from e
    

    def fit(self,X,y=None):
        return self

    def transform(self,X,y=None):
        try:
            room_per_household = X[:,self.total_room_ix] / X[:,self.households_ix]
            population_per_household = X[:,self.population_ix] / X[:,self.households_ix]

            if self.add_bedroom_per_room:
                bedrooms_per_room = X[:,self.total_bedrooms_ix] / X[:,self.total_room_ix]
                generated_features = np.c_[X,room_per_household,population_per_household,bedrooms_per_room]
            else:
                generated_features = np.c_[X,room_per_household,population_per_household]
                
            logging.info(f"Features Generated succesfully")
            return generated_features
        except Exception as e:
            raise HousingException(e,sys) from e

class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig
                ,data_ingestion_artifact:DataIngestionArtifact
                ,data_validation_artifact:DataValidationArtifact):
        try:
            logging.info(f"{'>>'*20}Data Tranformation log started.{'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact= data_validation_artifact
            self.train_file = self.data_ingestion_artifact.train_file
            self.test_file = self.data_ingestion_artifact.test_file
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_numerical_columns(self,X):
        try:
            self.numerical_columns_list = [col for col,colType in X.dtypes.iteritems() if colType != 'O']
            config = read_yaml(self.data_validation_artifact.schema_file_path)
            target_col = config[DATA_SET_SCHEMA_TARGET_COLUMN_KEY]
            self.numerical_columns_list.remove(target_col)
            return self.numerical_columns_list
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_categorical_columns(self,X):
        try:
            self.categorical_columns_list = [col for col,colType in X.dtypes.iteritems() if colType == 'O']
            return self.categorical_columns_list
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def get_null_numerical_columns(self,X):
        try:
            self.null_numerical_columns_list = [col for col,colType in X.dtypes.iteritems() if colType != 'O' and X[col].isna().sum() > 0]
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
    
    

    @staticmethod
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
    
    def get_data_tranformer_object(self)->ColumnTransformer:
        try:
            numerical_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy="median")),
                ('feature_generator',FeatureGenerator(
                        add_bedroom_per_room=self.data_transformation_config.add_bedroom_per_room,
                        columns=self.get_numerical_columns(X=pd.read_csv(self.data_ingestion_artifact.train_file)))),
                ('scaler',StandardScaler())
            ])

            categorical_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy="most_frequent")),
                ('encoding',OneHotEncoder()),
                ('scaler',StandardScaler(with_mean=False))
            ])

            preprocessing = ColumnTransformer([
                ('num_pipeline',numerical_pipeline,self.get_numerical_columns(X=pd.read_csv(self.data_ingestion_artifact.train_file))),
                ('cat_pipeline',categorical_pipeline,self.get_categorical_columns(X=pd.read_csv(self.data_ingestion_artifact.train_file)))
            ])

            return preprocessing
        except Exception as e:
            raise HousingException(e,sys) from e


    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            preprocessing_obj = self.get_data_tranformer_object()

            train_file = self.data_ingestion_artifact.train_file
            test_file = self.data_ingestion_artifact.test_file
            schema_file_path = self.data_validation_artifact.schema_file_path
            train_df = DataTransformation.load_data(file_path=train_file,schema_file_path=schema_file_path)
            test_df = DataTransformation.load_data(file_path=test_file,schema_file_path=schema_file_path)
            schema = read_yaml(file_path=schema_file_path)

            target_column_name = schema[DATA_SET_SCHEMA_TARGET_COLUMN_KEY]

            features_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_train_df = train_df[target_column_name]

            features_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_test_df = test_df[target_column_name]

            features_train_arr = preprocessing_obj.fit_transform(features_train_df)
            features_test_arr = preprocessing_obj.fit_transform(features_test_df)

            train_arr = np.c_[features_train_arr,np.array(target_train_df)]
            test_arr = np.c_[features_test_arr,np.array(target_test_df)]

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            transformed_train_filename = os.path.basename(train_file).replace(".csv",".npz")
            transformed_test_filename = os.path.basename(test_file).replace(".csv",".npz")

            transformed_train_filepath = os.path.join(transformed_train_dir,transformed_train_filename)
            transformed_test_filepath = os.path.join(transformed_test_dir,transformed_test_filename)

            save_array_data(filepath=transformed_train_filepath,array=train_arr)
            save_array_data(filepath=transformed_test_filepath,array=test_arr)
            preprocessed_object_file_path = self.data_transformation_config.preprocessed_object

            save_object_as_pkl(file_path=preprocessed_object_file_path,obj=preprocessing_obj)

            data_transformation_artifact=DataTransformationArtifact(transformed_train_file=transformed_train_filepath,
                                                                    transformed_test_file=transformed_test_filepath,
                                                                    preprocessed_file=preprocessed_object_file_path,
                                                                    is_transformed=True,
                                                                    message="Data transformation is done"
                                                                    )


            logging.info(f"Data Transformation Artifact : {data_transformation_artifact} ")

            return data_transformation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20}Data Transformation log Completed.{'<<'*20}")