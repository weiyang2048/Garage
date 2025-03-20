import pandas as pd
from sklearn.linear_model import LogisticRegression
import os
import sweetviz as sv
from ydata_profiling import ProfileReport
import logging
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif
import optuna
from sklearn.model_selection import cross_val_score
from catboost import CatBoostClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CreditScoringData:
    def __init__(self, data):
        self.data = data

    def fit(self, X_train, y_train):
        self.model = LogisticRegression()
        self.model.fit(X_train, y_train)

    def EDA(self, use="sweetviz"):
        if use == "sweetviz":
            report = sv.analyze(self.data)
            report.show_html("credit_scoring_sweetviz_report.html")
            logger.info("Sweetviz report saved to credit_scoring_sweetviz_report.html")
        elif use == "ydata":
            report = ProfileReport(self.data)
            report.to_file("credit_scoring_ydata_report.html")
            logger.info("Ydata report saved to credit_scoring_ydata_report.html")

    def encode_categorical_features(self):
        """
        Encodes categorical features in the dataset.
        """
        # Encode categorical features using one-hot encoding
        categorical_features = [
            "Month",
            "Occupation",
            "Type_of_Loan",
            "Changed_Credit_Limit",
            "Credit_Mix",
            "Payment_of_Min_Amount",
            "Payment_Behaviour",
        ]
        # as categorical
        self.data[categorical_features] = self.data[categorical_features].astype(
            "string"
        )

    def remove_personal_info(self):
        """
        Removes personal information from the dataset.
        """
        personal_info = ["ID", "Customer_ID", "Name", "SSN"]
        self.data = self.data.drop(columns=personal_info)


class CreditScoringPipeline:
    def __init__(self, data):
        """
        Initialize the credit scoring pipeline.

        Parameters
        ----------
        data : pandas.DataFrame
            Input dataset containing features and target
        """
        self.data = data
        self.best_params = None
        self.best_pipeline = None

    def create_pipeline(self, k1_features, catboost_params):
        """
        Create a pipeline with feature selection only for numerical features.

        Parameters
        ----------
        k1_features : int
            Number of top numerical features to select
        catboost_params : dict
            CatBoost parameters

        Returns
        -------
        sklearn.pipeline.Pipeline
            Configured pipeline
        """
        categorical_features = self.data.select_dtypes(
            include=["string"]
        ).columns.tolist()
        numerical_features = self.data.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

        # Create feature selector only for numerical features
        num_selector = SelectKBest(score_func=f_classif, k=k1_features)

        # Create a custom transformer to handle both feature types
        class FeatureSelector:
            def __init__(self, num_selector, cat_features, num_features):
                self.num_selector = num_selector
                self.cat_features = cat_features
                self.num_features = num_features

            def fit(self, X, y):
                if len(self.num_features) > 0:
                    self.num_selector.fit(X[self.num_features], y)
                return self

            def transform(self, X):
                selected_features = list(
                    self.cat_features
                )  # Use all categorical features
                if len(self.num_features) > 0:
                    num_mask = self.num_selector.get_support()
                    for i, feature in enumerate(self.num_features):
                        if num_mask[i]:
                            selected_features.append(feature)
                return X[selected_features]

        feature_selector = FeatureSelector(
            num_selector, categorical_features, numerical_features
        )

        pipeline = Pipeline(
            [
                ("feature_selector", feature_selector),
                (
                    "catboost",
                    CatBoostClassifier(
                        **catboost_params,
                        verbose=False,
                        cat_features=categorical_features,
                    ),
                ),
            ]
        )
        return pipeline

    def objective(self, trial):
        """
        Objective function for Optuna optimization.

        Parameters
        ----------
        trial : optuna.Trial
            Current trial object

        Returns
        -------
        float
            Mean cross-validation score
        """
        # Define the hyperparameters to optimize
        k1_features = trial.suggest_int(
            "k1_features",
            3,
            len(self.data.select_dtypes(include=["int64", "float64"]).columns),
        )

        catboost_params = {
            "iterations": trial.suggest_int("iterations", 100, 1000),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
            "depth": trial.suggest_int("depth", 3, 10),
            "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1, 10),
            "random_strength": trial.suggest_float("random_strength", 0.1, 10),
            "od_type": "Iter",
            "od_wait": trial.suggest_int("od_wait", 10, 50),
        }

        # Create and evaluate pipeline
        pipeline = self.create_pipeline(k1_features, catboost_params)
        scores = cross_val_score(
            pipeline,
            self.data.drop(columns=["Credit_Score"]),
            self.data["Credit_Score"],
            cv=5,
            scoring="accuracy",
            n_jobs=-1,
        )

        return scores.mean()

    def optimize(self, n_trials=100):
        """
        Optimize the pipeline using Optuna.

        Parameters
        ----------
        n_trials : int
            Number of optimization trials
        """
        study = optuna.create_study(direction="maximize")
        study.optimize(
            self.objective, n_trials=n_trials, n_jobs=-1, show_progress_bar=True
        )

        self.best_params = study.best_params
        self.best_pipeline = self.create_pipeline(
            self.best_params["k1_features"],
            {k: v for k, v in self.best_params.items() if k != "k1_features"},
        )

        logger.info(f"Best parameters: {self.best_params}")
        logger.info(f"Best cross-validation score: {study.best_value}")
        # get the best features
        self.best_features = self.best_pipeline.named_steps[
            "feature_selector"
        ].num_selector.get_support()
        logger.info(f"Best features: {self.best_features}")

    def fit(self):
        """
        Fit the best pipeline on the entire dataset.
        """
        if self.best_pipeline is None:
            raise ValueError("Pipeline not optimized yet. Call optimize() first.")

        X = self.data.drop(columns=["Credit_Score"])
        y = self.data["Credit_Score"]
        self.best_pipeline.fit(X, y)

    def predict(self, X):
        """
        Make predictions using the fitted pipeline.

        Parameters
        ----------
        X : pandas.DataFrame
            Features to predict on

        Returns
        -------
        numpy.ndarray
            Predicted credit scores
        """
        if self.best_pipeline is None:
            raise ValueError("Pipeline not fitted yet. Call fit() first.")

        return self.best_pipeline.predict(X)


def main(EDA=False, n_trials=50):
    """
    The main function to create an instance of the CreditScoringModel class and display
    the first few rows of the dataset.
    """
    # Create an instance of the CreditScoringModel class and pass the data
    data = pd.read_csv(
        os.path.join("Data Sets", "Finance", "credit_scoring_full.csv"), header=0
    )

    CreditModel = CreditScoringData(data)

    CreditModel.encode_categorical_features()
    CreditModel.remove_personal_info()
    if EDA:
        CreditModel.EDA(use="ydata")

    pipeline = CreditScoringPipeline(CreditModel.data)
    pipeline.optimize(n_trials=n_trials)  # Adjust number of trials as needed
    pipeline.fit()
    predictions = pipeline.predict(CreditModel.data.drop(columns=["Credit_Score"]))
    # display the predictions
    print(predictions)


if __name__ == "__main__":
    # get the argument from the command line
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--EDA", type=bool, default=False)
    parser.add_argument("--n_trials", type=int, default=50)
    args = parser.parse_args()
    main(EDA=args.EDA, n_trials=args.n_trials)
