import pandas as pd
from datetime import datetime
from ._base import DataFrameFromJSONMixin


class Patients(DataFrameFromJSONMixin):
    def __init__(self, path):
        super().__init__(path)

    def get_age(self, dob, input_date="2023-11-05"):
        """
        Question 1-1
        Calculate the age of the patient.

        Create a function that calculates the age based on the birthday and a given date. This will be used to apply to each row of the
        patient dataframe.

        For example if the dob is 2000-01-01 and the input_date is 2024-01-03 then the age is 24

        inputs:
        dob: string birthdate of patient
        input_date: string date used to calculate the age. yyyy-mm-dd

        Output:
        age_years: integer the age of the patient in years
        """
        # TODO: Implement age calculation
        # Hint: Use datetime.strptime() to parse the birthDate and calculate age from current date
        # The birthDate format is 'YYYY-MM-DD'

        dob_dt = datetime.strptime(dob, "%Y-%m-%d")
        input_dt = datetime.strptime(input_date, "%Y-%m-%d")

        age = input_dt.year - dob_dt.year
        if (input_dt.month, input_dt.day) < (dob_dt.month, dob_dt.day):
            age -= 1

        return age

    def get_marital_status(self, df: pd.DataFrame):
        """
        Question 1-2
        One hot encode the marital status. Take the existing dataframe and add the marital status columns.
         You can use built in pandas function for this.

        The columns added should be the following. It should be an integer 0 or 1.
        married_Divorced

        married_Married

        married_Never Married

        married_Widowed


        Input: pandas dataframe
        Output: pandas dataframe
        """
        # TODO: Implement marital status one-hot encoding
        # Hint: Use pd.get_dummies() to create one-hot encoded columns
        # Make sure to handle the nested structure of maritalStatus (it's a dict with 'text' field)

        df = df.copy()

        df["marital_status_text"] = df["maritalStatus"].apply(
            lambda x: x.get("text") if isinstance(x, dict) else None
        )

        dummies = pd.get_dummies(df["marital_status_text"], prefix="married").astype(
            int
        )

        required_cols = [
            "married_Divorced",
            "married_Married",
            "married_Widowed",
            "married_Never Married",
        ]

        for col in required_cols:
            if col not in dummies.columns:
                dummies[col] = 0

        df = pd.concat([df, dummies[required_cols]], axis=1)

        return df

    def pipeline(self):
        """
        Complete pipeline for processing patient data.
        This combines both age calculation and marital status encoding.
        """
        patient_df = self.data.copy()

        # Exercise 1-1: Calculate age
        patient_df["age"] = patient_df["birthDate"].apply(self.get_age)

        # Exercise 1-2: One-hot encode marital status
        patient_df = self.get_marital_status(patient_df)

        return patient_df[
            [
                "id",
                "age",
                "married_Divorced",
                "married_Married",
                "married_Widowed",
                "married_Never Married",
            ]
        ]
