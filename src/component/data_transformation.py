import os
import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils import save_object
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    # Fixed: Typo correction from original instantiation pattern
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor_obj.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transforamtion_config = DataTransformationConfig()

    # FIX 2: Removed unused train_data, test_data arguments to keep it clean
    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    # Set sparse_output=False so it returns a dense numpy array smoothly
                    ("onehot", OneHotEncoder(sparse_output=False))
                ]
            )

            logging.info("Numerical column standard scaling completed.")
            logging.info("Categorical column encoding completed.")

            # FIX 1: Cleaned up ColumnTransformer tuples
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed.")
            logging.info("Obtaining preprocessing object.")

            # Called cleanly without unnecessary empty arguments
            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math_score"

            # Isolating features from target
            input_feature_train_df = train_df.drop(columns=[target_column_name])
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name])
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on train and test dataframes.")

            # Running pipelines
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Recombining features and labels into standalone arrays using np.c_
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info("Saving preprocessed transformer object.")

            # This will trigger your utility helper to write to the artifacts folder
            save_object(
                file_path=self.data_transforamtion_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transforamtion_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)