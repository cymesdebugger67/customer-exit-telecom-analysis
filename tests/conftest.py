import sys
from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT / "src"),
)


@pytest.fixture
def sample_raw():
    return pd.DataFrame(
        {
            "customerID": [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
            ],
            "gender": [
                "Female",
                "Male",
                "Female",
                "Male",
                "Female",
                "Male",
            ],
            "SeniorCitizen": [
                0,
                1,
                0,
                1,
                0,
                0,
            ],
            "Partner": [
                "Yes",
                "No",
                "Yes",
                "No",
                "No",
                "Yes",
            ],
            "Dependents": [
                "No",
                "No",
                "Yes",
                "No",
                "No",
                "Yes",
            ],
            "tenure": [
                1,
                8,
                18,
                36,
                60,
                0,
            ],
            "PhoneService": [
                "Yes",
                "Yes",
                "Yes",
                "Yes",
                "Yes",
                "Yes",
            ],
            "MultipleLines": [
                "No",
                "Yes",
                "No",
                "Yes",
                "No",
                "No",
            ],
            "InternetService": [
                "DSL",
                "Fiber optic",
                "Fiber optic",
                "DSL",
                "No",
                "No",
            ],
            "OnlineSecurity": [
                "No",
                "No",
                "Yes",
                "Yes",
                "No internet service",
                "No internet service",
            ],
            "OnlineBackup": [
                "No",
                "Yes",
                "Yes",
                "Yes",
                "No internet service",
                "No internet service",
            ],
            "DeviceProtection": [
                "No",
                "No",
                "Yes",
                "Yes",
                "No internet service",
                "No internet service",
            ],
            "TechSupport": [
                "No",
                "No",
                "Yes",
                "Yes",
                "No internet service",
                "No internet service",
            ],
            "StreamingTV": [
                "No",
                "Yes",
                "Yes",
                "No",
                "No internet service",
                "No internet service",
            ],
            "StreamingMovies": [
                "No",
                "Yes",
                "Yes",
                "No",
                "No internet service",
                "No internet service",
            ],
            "Contract": [
                "Month-to-month",
                "Month-to-month",
                "One year",
                "One year",
                "Two year",
                "Two year",
            ],
            "PaperlessBilling": [
                "Yes",
                "Yes",
                "Yes",
                "No",
                "No",
                "No",
            ],
            "PaymentMethod": [
                "Electronic check",
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
                "Mailed check",
            ],
            "MonthlyCharges": [
                30.0,
                85.0,
                95.0,
                65.0,
                25.0,
                20.0,
            ],
            "TotalCharges": [
                "30",
                "680",
                "1710",
                "2340",
                "1500",
                " ",
            ],
            "Churn": [
                "Yes",
                "Yes",
                "No",
                "No",
                "No",
                "No",
            ],
        }
    )
