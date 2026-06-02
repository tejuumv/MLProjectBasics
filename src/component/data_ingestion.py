import os
import sys
from src.exception import CustomException
from src.logger import logging

import pandas as pd
# FIX 1: Corrected the train_test_split import
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.component.data_transformation import DataTransformation
from src.component.data_transformation import DataTransformationConfig

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "data.csv")


class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    # FIX 2: Removed @property so it acts as an executable method
    def initiate_data_ingestion(self):
        logging.info("Initiating data ingestion")
        try:
            # Cross-platform safe path syntax
            csv_path = os.path.join("notebook", "data", "stud.csv")
            df = pd.read_csv(csv_path)
            logging.info("Read the DataFrame successfully")

            # Creating the artifacts directory
            os.makedirs(os.path.dirname(self.data_ingestion_config.train_data_path), exist_ok=True)

            # Saving raw data
            df.to_csv(self.data_ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train Test Split Initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Saving split sets
            train_set.to_csv(self.data_ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion Completed successfully")

            return (
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e, sys)


# To run and verify it builds the artifacts:
if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)