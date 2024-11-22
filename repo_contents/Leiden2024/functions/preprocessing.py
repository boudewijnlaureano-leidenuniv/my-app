import pandas as pd
import numpy as np 

class DataExploration:  
  
    @staticmethod  
    def display_nans(df):  
        for col in df.columns:  
            print(f"{col}: {df[col].isna().sum()} NaN values")  

    @staticmethod
    def fill_nans(df):  
        for col in df.columns:  
            if df[col].dtype == np.number:  
                df[col].fillna(df[col].mean(), inplace=True)  
            else:  
                df[col].fillna(df[col].mode()[0], inplace=True)  
        return df  