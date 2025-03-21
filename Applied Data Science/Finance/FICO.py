import os
import sweetviz as sv
from ydata_profiling import ProfileReport
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif, chi2
import numpy as np

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FICO:
    """
    A class to represent the FICO credit scoring system.

    Attributes:
        data (pandas.DataFrame): The dataset containing credit information.
        education_level_mapping (dict): A dictionary mapping education levels to numerical values.
        employment_status_mapping (dict): A dictionary mapping employment statuses to numerical values.

    Methods:
        EDA(use="sweetviz"): Performs exploratory data analysis using Sweetviz or ydata_profiling.
        calculate_credit_scores(): Calculates credit scores based on the FICO formula.
        select_features(X, y, k1=3, k2=2): Selects features using SelectKBest for both numerical and categorical features separately.
    """

    def __init__(self, data):
        """
        Constructs all the necessary attributes for the FICO object.

        Parameters:
            data (pandas.DataFrame): The dataset containing credit information.
        """
        self.data = data
        self.education_level_mapping = {
            "High School": 1,
            "Bachelor": 2,
            "Master": 3,
            "PhD": 4,
        }
        self.employment_status_mapping = {
            "Unemployed": 0,
            "Employed": 1,
            "Self-Employed": 2,
        }
        self.data["Education Level"] = self.data["Education Level"].map(self.education_level_mapping)
        self.data["Employment Status"] = self.data["Employment Status"].map(self.employment_status_mapping)

    def EDA(self, use="sweetviz"):
        """
        Performs exploratory data analysis on the dataset using Sweetviz or ydata_profiling
        and generates an HTML report.

        Parameters:
            use (str): The tool to use for EDA, either "sweetviz" or "ydata".
        """
        if use == "sweetviz":
            report = sv.analyze(self.data)
            report.show_html("credit_scoring_sweetviz_report.html")
        elif use == "ydata":
            report = ProfileReport(self.data)
            report.to_notebook_iframe()

    def calculate_credit_scores(self):
        """
        Calculates credit scores for each entry in the dataset using the FICO formula
        and adds them to the dataset.
        """
        credit_scores = []
        for index, row in self.data.iterrows():
            payment_history = row["Payment History"]
            credit_utilization_ratio = row["Credit Utilization Ratio"]
            number_of_credit_accounts = row["Number of Credit Accounts"]
            education_level = row["Education Level"]
            employment_status = row["Employment Status"]

            # Apply the FICO formula to calculate the credit score
            credit_score = (
                (payment_history * 0.35)
                + (credit_utilization_ratio * 0.30)
                + (number_of_credit_accounts * 0.15)
                + (education_level * 0.10)
                + (employment_status * 0.10)
            )
            credit_scores.append(credit_score)

        self.data["Credit Score"] = credit_scores

    def select_features(self, X, y, k1=3, k2=2):
        """
        Selects features using SelectKBest for both numerical and categorical features separately.
        
        Parameters:
            X (pandas.DataFrame): Feature matrix
            y (pandas.Series): Target variable
            k1 (int): Number of numerical features to select
            k2 (int): Number of categorical features to select
            
        Returns:
            list: Selected feature names
        """
        # Separate numerical and categorical columns
        numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
        categorical_features = X.select_dtypes(include=['object', 'category']).columns
        
        selected_features = []
        
        # Handle numerical features
        if len(numerical_features) > 0:
            selector_num = SelectKBest(score_func=f_classif, k=min(k1, len(numerical_features)))
            X_num = X[numerical_features]
            selector_num.fit(X_num, y)
            
            # Get selected numerical features
            selected_num_features = X_num.columns[selector_num.get_support()].tolist()
            selected_features.extend(selected_num_features)
            
        # Handle categorical features
        if len(categorical_features) > 0:
            selector_cat = SelectKBest(score_func=chi2, k=min(k2, len(categorical_features)))
            X_cat = X[categorical_features]
            selector_cat.fit(X_cat, y)
            
            # Get selected categorical features
            selected_cat_features = X_cat.columns[selector_cat.get_support()].tolist()
            selected_features.extend(selected_cat_features)
            
        logger.info(f"Selected numerical features: {selected_num_features if 'selected_num_features' in locals() else []}")
        logger.info(f"Selected categorical features: {selected_cat_features if 'selected_cat_features' in locals() else []}")
        
        return selected_features

def main():
    """
    The main function to create an instance of the FICO class and display
    the first few rows of the dataset.
    """
    # Create an instance of the FICO class and pass the data
    data = pd.read_csv(os.path.join("..", "Data Sets", "finance", "credit_scoring.csv"))
    fico = FICO(data)
    fico.EDA(use="ydata")
    fico.calculate_credit_scores()
    fico.EDA(use="sweetviz")

if __name__ == "__main__":
    main()
