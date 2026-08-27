import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
    filemode="a"
)

engine=create_engine('sqlite:///inventory.db')

def ingest_db(df,table_name,engine):
    df.to_sql(table_name,engine,if_exists='replace',index=False)

def load_raw_data():
    '''this function loads the raw data from the data folder and ingests it into the database'''
    start=time.time();
    for file in os.listdir('data') :
        if '.csv' in file:
            df=pd.read_csv('data/'+file)
            ingest_db(df,file[:-4],engine)
            logging.info(f"Data loaded for {file[:-4]} with shape {df.shape}")
    end=time.time();
    total_time=(end-start)/60
    logging.info("Data ingestion completed successfully.")
    logging.info(f"Total time taken for data ingestion: {total_time} minutes")

if __name__=="__main__":
    load_raw_data()