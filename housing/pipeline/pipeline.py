
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.data_transformation import DataTransformation
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from housing.logger import logging
from housing.exception import HousingException
from housing.config.configuration import Configuration
import os,sys

class Pipeline:
    def __init__(self,config = Configuration()):

        self.config = config

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info(f"{'--'*20}Data ingestion pipeline started{'--'*20}")
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            logging.info(f"{'--'*20}Data ingestion pipeline ended{'--'*20}")
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise HousingException(e,sys) from e

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact )->DataValidationArtifact:
        try:
            logging.info(f"{'--'*20}Data validation pipeline started{'--'*20}")
            data_validation_config=self.config.get_data_validation_config()
            data_validation=DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
            logging.info(f"{'--'*20}Data validation pipeline ended{'--'*20}")
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise HousingException(e,sys) from e
            
    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            logging.info(f"{'--'*20}Data transformation pipeline started{'--'*20}")
            data_transformation_config = self.config.get_data_transformation_config()
            data_transformation = DataTransformation(data_transformation_config=data_transformation_config
                                ,data_ingestion_artifact=data_ingestion_artifact,
                                data_validation_artifact=data_validation_artifact)
        
            logging.info(f"{'--'*20}Data transformation pipeline ended{'--'*20}")
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise HousingException(e,sys) from e

    def run_pipeline(self):
        try:
            logging.info(f"{'##'*20} Pipeline Started.{'##'*20}")
            #Data ingestion
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                            data_validation_artifact=data_validation_artifact)
            
        except Exception as e:
            raise HousingException(e,sys) from e

        
    def __del__(self):
        logging.info(f"{'##'*20} Pipeline ended.{'##'*20}")


