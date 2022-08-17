
from housing.exception import HousingException
from housing.pipeline.pipeline import Pipeline
from housing.utils.utils import *
from housing.component.data_transformation import DataTransformation
#from housing.entity.config_entity import DataTransformationConfig
from housing.config.configuration import Configuration
import sys
try:
    #train_file  = r"C:\Users\khush\Desktop\ML_Project\ml_project\housing\arifact\data_ingestion\2022-08-13-14-06-00\ingested_data\train\housing.csv"
    #dump_yaml(file_path=train_file)
    #Pipeline().run_pipeline()
    schema = r"C:\Users\khush\Desktop\ML_Project\ml_project\config\schema.yaml"
    file = r"C:\Users\khush\Desktop\ML_Project\ml_project\housing\artifact\data_ingestion\2022-08-15-20-31-32\ingested_data\train\housing.csv"
    df = DataTransformation.load_data(file_path=file,schema_file_path=schema)
    print(df.dtypes)
    #data_ingestion_config = config.get_data_ingestion_config()
    #data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    #data_ingestion.start_data_ingestion()
except Exception as e:
    raise HousingException(e,sys) from e
    


