from ._base import DataFrameFromJSONMixin
import pandas as pd


def get_patientid(subject):
    """
    Helper function to get a patient id from a FHIR reference string.
    """
    split_string = subject["reference"].split("/")
    return split_string[-1]


class Observations(DataFrameFromJSONMixin):
    def __init__(self, path, patient_path):
        super().__init__(path)
        self.patient_df = pd.read_json(patient_path, lines=True)

    def impute_observation(
        self,
        obs_df: pd.DataFrame,
        patient_df: pd.DataFrame,
        loinc_code: str,
        col_name: str,
    ):
        """
        Question 2

        Impute missing data for the glucose and triglycerides by using the mean of the column.
        You will be using the observation resources that have these values.
        You will be creating a column that that is a numerical value of the observation.
        You will need to group the observation records by patient id.
        When using the aggregation function aggregate by mean. The mean should be rounded to 2 decimal places

        The Loinc code for glucose is "2339-0"
        The Loinc code for triglycerides is "2571-8"

        Input: observations dataframe, loinc_code, col_name
        Output: a pandas dataframe grouped by patient id with mean imputed values for target column
        """
        # TODO: Implement observation imputation
        # Steps:
        # 1. Extract patient IDs from subject references
        # 2. Filter observations by LOINC code
        # 3. Extract numerical values from valueQuantity
        # 4. Group by patient ID and calculate mean
        # 5. Merge with patient DataFrame
        # 6. Impute missing values with column mean
        # 7. Round to 2 decimal places

        df = obs_df.copy()

        df["id"] = df["subject"].apply(get_patientid)

        df = df[
            df["code"].apply(
                lambda x: any(c.get("code") == loinc_code for c in x.get("coding", []))
            )
        ]

        df[col_name] = df["valueQuantity"].apply(
            lambda x: x.get("value") if isinstance(x, dict) else None
        )

        grouped = df.groupby("id")[col_name].mean().reset_index()

        merged = patient_df[["id"]].merge(grouped, on="id", how="left")

        mean_val = merged[col_name].mean()
        merged[col_name] = merged[col_name].fillna(mean_val)

        merged[col_name] = merged[col_name].round(2)

        return merged

    def mean_normalize(self, df: pd.DataFrame, col_name: str):
        """
        Question 3
        Create a function that will apply z score mean normalization to a column
        round the result to 3 decimal places. Hint this uses standard deviation. This function will take a dataframe
        and the column name. It will apply normalization to the to the specified column.

        Inputs:
        df: is a dataframe
        col_name:  the column name that z score mean normalized is applied to

        Output: pandas series data float 3 decimal places
        """
        # TODO: Implement mean normalization (z-score standardization)
        # Formula: (x - mean) / standard_deviation
        # Round the result to 3 decimal places

        mean = df[col_name].mean()
        std = df[col_name].std()

        normalized = (df[col_name] - mean) / std

        return normalized.round(3)

    def pipeline(self):
        """
        Complete pipeline for processing observation data.
        This combines imputation and normalization.
        """
        observation_df = self.data
        patient_df = self.patient_df

        # Exercise 2: Get imputed values for glucose and triglycerides
        observation_glucose_df = self.impute_observation(
            observation_df, patient_df, "2339-0", "glucose"
        )
        observation_tri_df = self.impute_observation(
            observation_df, patient_df, "2571-8", "triglycerides"
        )

        # Merge the glucose and triglycerides dataframes
        combined_df = observation_tri_df.merge(
            observation_glucose_df, how="left", on="id"
        )

        # Exercise 3: Apply mean normalization to the glucose and triglycerides columns
        combined_df["glucose"] = self.mean_normalize(combined_df, "glucose")
        combined_df["triglycerides"] = self.mean_normalize(combined_df, "triglycerides")

        return combined_df[["id", "glucose", "triglycerides"]]
