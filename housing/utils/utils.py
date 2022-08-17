from housing.logger import logging
from housing.exception import HousingException
import sys
import yaml
import pandas as pd

def read_yaml(file_path:str) -> dict:
    """
    This function read yaml file and return dict
    file_path : Str
    returns : Dict
    """
    try:
        with open(file_path,'rb') as file:
            logging.info(f"Reading yaml file from : [ {file_path} ]")
            return yaml.safe_load(file)
    except Exception as e:
        raise HousingException(e,sys) from e

def dump_yaml(file_path:str)-> None:
    """
    This function dynamically create schema file out of panda data frame

    file_path : str
    returns : Dict

    """

    try:
        df = pd.read_csv(file_path)
        #print(df.head())
        col = df.columns
        #print(col)
        type = list(map(lambda x:str(x).replace("dtype('","").replace("')",""),df.dtypes.values))
        #print(type)
        col_dic = dict(zip(col,type))
        #print(col_dic)
        

        for i in col_dic.keys():
            if col_dic[i] == 'object':
                col_dic[i+'1'] = df[i].unique()
                break
        #print(col_dic)
        with open(r"C:\Users\khush\Desktop\ML_Project\ml_project\config\schema.yaml",'w') as file:
            yaml.dump(col_dic,file,indent=2)

    except Exception as e:
        raise HousingException(e,sys) from e    