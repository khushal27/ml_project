from housing.exception import HousingException
from housing.logger import logging
from housing.constant import *
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import os,sys
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import pandas as pd
import json

class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20}Data Validation log started.{'<<'*20} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise HousingException(e,sys) from e

    def file_availability_validation(self):
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def file_type_validation(self):
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e

    def is_schema_validation(self):
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e

    def domain_value_validation(self):
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e   

    def null_data_validation(self):
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e       

    def get_and_save_data_drift_report(self):
        try:
            train_data = self.data_ingestion_artifact.train_file
            test_data = self.data_ingestion_artifact.test_file
            #test_data = r"C:\Users\khush\Desktop\ML_Project\ml_project\housing\artifact\data_ingestion\2022-08-15-10-04-21\ingested_data\test\housing.csv"
            
            train_df = pd.read_csv(train_data)
            test_df = pd.read_csv(test_data)
            
            
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference_data=train_df,current_data=test_df)

            report = json.loads(data_drift_profile.json())
            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as file:
                json.dump(report,file,indent=6)

            return report


        except Exception as e:
            raise HousingException(e,sys) from e       

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])

            train_data = self.data_ingestion_artifact.train_file
            test_data = self.data_ingestion_artifact.test_file
            #test_data = r"C:\Users\khush\Desktop\ML_Project\ml_project\housing\artifact\data_ingestion\2022-08-15-10-04-21\ingested_data\test\housing.csv"
            train_df = pd.read_csv(train_data)
            test_df = pd.read_csv(test_data)

            dashboard.calculate(reference_data=train_df,current_data=test_df)
            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise HousingException(e,sys) from e       


    def is_data_drift_found(self):
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()

            return True
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_data_drift_found()
            report = self.data_validation_config.report_file_path
            report_page = self.data_validation_config.report_page_file_path
            data_validation_artifact = DataValidationArtifact(report=report,report_page=report_page,
            is_validated=True,message="Data validation completed!")

            logging.info(f"Data Validation Artifact : [ {data_validation_artifact} ]")
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e


    def __del__(self):
        logging.info(f"{'>>'*20}Data Validation log completed.{'<<'*20} \n\n")

