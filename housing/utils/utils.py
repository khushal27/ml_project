from housing.logger import logging
from housing.exception import HousingException
import sys,os
import yaml
import pandas as pd
import numpy as np
import dill
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


def save_array_data(filepath:str,array:np.array):
    """
    This util function save numpy array into file
    filepath :str
    array : np.array
    """
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path,exist_ok=True)
        with open(filepath,"wb") as np_file:
            np.save(np_file,array)
    except Exception as e:
        raise HousingException(e,sys) from e    


def save_object_as_pkl(file_path:str , obj):
    """
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,"wb") as file_object:
            dill.dump(obj,file_object)
    except Exception as e:
        raise HousingException(e,sys) from e  