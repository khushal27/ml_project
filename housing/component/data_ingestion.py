
from housing.entity.config_entity import DataIngestionConfig
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.exception import HousingException
import tarfile
from six.moves import urllib 
from housing.logger import logging
import os,sys
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit


class DataIngestion:
    
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log Started.{'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e  

    def download_data(self):
        try:
            # URL
            download_url = self.data_ingestion_config.dataset_download_url

            #getting the folder loaction to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            #create folder if not exists
            os.makedirs(tgz_download_dir,exist_ok=True)

            #basefile name
            tgz_filename = os.path.basename(download_url)

            tgz_file_path = os.path.join(tgz_download_dir,tgz_filename)

            logging.info(f"Downloading data from URL : {download_url} into DIR : {download_url}")
            urllib.request.urlretrieve(download_url,tgz_file_path)
            logging.info(f"Data downloaded at : {tgz_file_path}")

            return tgz_file_path

        except Exception as e:
            raise HousingException(e,sys) from e  

    def extract_tgz_file(self,tgz_filepath:str):

         try:
            
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            os.makedirs(raw_data_dir,exist_ok=True)
            
            logging.info(f"Extracting file from [ {tgz_filepath} ] into DIR : [ {raw_data_dir} ]")
            with tarfile.open(tgz_filepath) as tgz_file_obj:
                tgz_file_obj.extractall(path=raw_data_dir)
            logging.info(f"Extraction completed!!!")

            return raw_data_dir

         except Exception as e:
            raise HousingException(e,sys) from e  

    def split_data_train_test(self,raw_data_dir:str) -> DataIngestionArtifact:
        try:
            raw_data_file_name = os.listdir(raw_data_dir)[0]

            train_data_dir = self.data_ingestion_config.ingested_train_dir
            os.makedirs(train_data_dir,exist_ok=True)

            test_data_dir = self.data_ingestion_config.ingested_test_dir
            os.makedirs(test_data_dir,exist_ok=True)

            housing_raw_file_path = os.path.join(raw_data_dir,raw_data_file_name)

            housing_data_df = pd.read_csv(housing_raw_file_path)

            #for split
            housing_data_df["income_cat"] = pd.cut(
                housing_data_df["median_income"],
                bins=[0.0,1.5,3.0,4.5,6.0,np.inf],
                labels=[1,2,3,4,5]
            )

            strat_train_data = None
            strat_test_data = None
            
            split = StratifiedShuffleSplit(n_splits=1,test_size=0.20,random_state=42)

            for train_index,test_index in split.split(housing_data_df,housing_data_df["income_cat"]):
                strat_train_data = housing_data_df.loc[train_index].drop(["income_cat"],axis=1)
                strat_test_data = housing_data_df.loc[test_index].drop(["income_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,raw_data_file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,raw_data_file_name)

            logging.info(f"saving training file at : [ {train_file_path} ]")
            strat_train_data.to_csv(train_file_path,index=False)

            logging.info(f"saving testing file at : [ {test_file_path} ]")
            strat_test_data.to_csv(test_file_path,index=False)
        
            data_ingestion_artifact = DataIngestionArtifact(train_file=train_file_path,
                                    test_file=test_file_path,
                                    is_ingested=True,
                                    message="Data ingestion and split completed!!!")
            logging.info(f"Data ingestion Artifact : [ {data_ingestion_artifact} ]")
            return data_ingestion_artifact
        except Exception as e:
            raise HousingException(e,sys) from e  

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_data()
            raw_data_dir = self.extract_tgz_file(tgz_file_path)
            data_ingestion_artifact = self.split_data_train_test(raw_data_dir)
            return data_ingestion_artifact

        except Exception as e:
            raise HousingException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log Completed.{'<<'*20}")


