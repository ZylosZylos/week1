from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass
class LogisticRegressionConfig:
    target_column: str
    test_size: float = 0.2
    random_state: int = 42
    max_iter: int = 1000
    solver: str = "lbfgs"
    class_weight: str | dict[str, float] | None = None
    stratify: bool = True
    threshold: float = 0.5


class LogisticRegressionTemplate:
    def __init__(self, config: LogisticRegressionConfig) -> None:
        self.config = config
        self.pipeline: Pipeline | None = None
        self.feature_columns: list[str] = []

    def _build_pipeline(self, X: pd.DataFrame) -> Pipeline:
        numeric_features = X.select_dtypes(include=["number"]).columns.tolist()
        categorical_features = X.select_dtypes(exclude=["number"]).columns.tolist()

        numeric_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        categorical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_pipeline, numeric_features),
                ("cat", categorical_pipeline, categorical_features),
            ]
        )

        model = LogisticRegression(
            max_iter=self.config.max_iter,
            solver=self.config.solver,
            class_weight=self.config.class_weight,
        )

        return Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )

    def fit(self, data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
        if self.config.target_column not in data.columns:
            raise ValueError(f"Target column '{self.config.target_column}' not found in data.")

        X = data.drop(columns=[self.config.target_column]).copy()
        y = data[self.config.target_column].copy()

        self.feature_columns = X.columns.tolist()
        self.pipeline = self._build_pipeline(X)

        stratify_target = y if self.config.stratify else None

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=self.config.test_size,
            random_state=self.config.random_state,
            stratify=stratify_target,
        )

        self.pipeline.fit(X_train, y_train)
        return X_train, y_train, X_test, y_test

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict[str, Any]:
        if self.pipeline is None:
            raise ValueError("Model has not been trained yet. Please call fit() first.")

        y_pred = self.pipeline.predict(X_test)
        result: dict[str, Any] = {
            "accuracy": accuracy_score(y_test, y_pred),
            "confusion_matrix": confusion_matrix(y_test, y_pred),
            "classification_report": classification_report(y_test, y_pred, zero_division=0),
        }

        if hasattr(self.pipeline, "predict_proba") and len(pd.Series(y_test).unique()) == 2:
            y_prob = self.pipeline.predict_proba(X_test)[:, 1]
            result["roc_auc"] = roc_auc_score(y_test, y_prob)

        return result

    def predict(self, new_data: pd.DataFrame) -> pd.Series:
        if self.pipeline is None:
            raise ValueError("Model has not been trained yet. Please call fit() first.")
        return pd.Series(self.pipeline.predict(new_data), name="prediction")

    def predict_proba(self, new_data: pd.DataFrame) -> pd.DataFrame:
        if self.pipeline is None:
            raise ValueError("Model has not been trained yet. Please call fit() first.")
        if not hasattr(self.pipeline, "predict_proba"):
            raise ValueError("Current model does not support probability prediction.")

        probabilities = self.pipeline.predict_proba(new_data)
        class_names = [f"class_{label}_prob" for label in self.pipeline.named_steps["model"].classes_]
        return pd.DataFrame(probabilities, columns=class_names)

    def save(self, model_path: str | Path) -> None:
        if self.pipeline is None:
            raise ValueError("Model has not been trained yet. Please call fit() first.")
        joblib.dump({"pipeline": self.pipeline, "feature_columns": self.feature_columns}, model_path)

    @staticmethod
    def load(model_path: str | Path) -> dict[str, Any]:
        return joblib.load(model_path)


def load_csv(csv_path: str | Path) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def run_example() -> None:
    """
    使用说明:
    1. 准备一个 CSV 文件，例如 data.csv
    2. 将 target_column 改成你的标签列名
    3. 运行 `python codextest.py`
    """

    csv_path = "data.csv"
    target_column = "target"

    data = load_csv(csv_path)

    trainer = LogisticRegressionTemplate(
        LogisticRegressionConfig(
            target_column=target_column,
            test_size=0.2,
            random_state=42,
            max_iter=1000,
            solver="lbfgs",
            class_weight=None,
        )
    )

    _, _, X_test, y_test = trainer.fit(data)
    metrics = trainer.evaluate(X_test, y_test)

    print("Accuracy:", metrics["accuracy"])
    if "roc_auc" in metrics:
        print("ROC-AUC:", metrics["roc_auc"])
    print("Confusion Matrix:\n", metrics["confusion_matrix"])
    print("Classification Report:\n", metrics["classification_report"])

    trainer.save("logistic_regression_model.joblib")


if __name__ == "__main__":
    run_example()
