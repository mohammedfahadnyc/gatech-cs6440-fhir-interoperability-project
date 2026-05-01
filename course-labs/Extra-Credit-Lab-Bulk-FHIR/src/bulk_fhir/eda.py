from datetime import date
from typing import Tuple
import pandas as pd
import numpy as np


def count_all_prediabetes(df: pd.DataFrame) -> int:
    """
    Q1. Counts the number of patients with a condition of prediabetes.

    Parameters
    ----------
    df : DataFrame
        Original Pandas DataFrame that has the bulk fhir export from the dataloader

    Prediabetes is represented as SNOMED code: 15777000

    Note: This is a deprecated SNOMED Code, but it is what appears in the data set.
    You will not find it in current versions of the SNOMED browser.

    Hint: You can access the "Condition.code" element from the Pandas Dataframe using "data['code']".
    Keep in mind that this is a nested JSON object inside the Dataframe. EXAMPLE: print(data['code'][0])

    Hint 2: While it is not generally recommended to iterate over a Pandas Dataframe for performance reasons,
    you are allowed to do so here for simplicity.

    """
    snomed = "15777000"
    # TODO Write your code here. Below is mostly just placeholder code to get you started.
    code = df["code"]

    count = 0
    for c in code:
        if isinstance(c, dict):
            codings = c.get("coding", [])
            for item in codings:
                if str(item.get("code")) == snomed:
                    count += 1
                    break

    return count


def count_prediabetes_timerange(
    df: pd.DataFrame, start_year: int, end_year: int
) -> int:
    """
    Q2. Counts the number of patients with a condition of prediabetes in a range of years

    Parameters
    ----------
    df: DataFrame
        Original Pandas DataFrame that has the bulk fhir export from the dataloader
    start_year: int
        Lower bound year of the range
    end_year: int
        Upper bound year of the range

    Note: You may reuse the code written in Q1

    Hint: You may use the date in the builtin datetime package if you'd like.
    """
    snomed = "15777000"
    # TODO Write your code here. Below is mostly just placeholder code to get you started.
    code = df["code"]
    recorded_date = df["recordedDate"]

    count = 0

    for _, row in df.iterrows():
        code_obj = row["code"]
        recorded = row["recordedDate"]

        has_prediabetes = False

        if isinstance(code_obj, dict):
            codings = code_obj.get("coding", [])
            for item in codings:
                if str(item.get("code")) == snomed:
                    has_prediabetes = True
                    break

        if has_prediabetes and isinstance(recorded, str):
            year = int(recorded[:4])
            if start_year <= year <= end_year:
                count += 1

    return count


def predict_future_cumulative_prediabetes(df: pd.DataFrame, year: int) -> float:
    """
    Q3. Create a linear regression line of cumulative number of patients that had a condition of prediabetes
    and predict the cumulative number of patients for a given year.

    Note that by cumulative this means the line should always be increasing or plateauing.

    NOTE: Only stick to native Python, numpy or pandas methods to create linear regression coefficients.
    The autograder environment will have numpy and pandas, but not scipy, sklearn, etc.

    Parameters
    ----------
    df: DataFrame
        Original Pandas DataFrame that has the bulk fhir export from the dataloader
    year: int
        Year of interest to predict the cumulative number of patients for.

    Hint: Treat the years as X and cumulative num of patients as Y

    Hint 2: Use simple linear regression bX + a = Y

    Hint 3: You may use a custom python function to calculate coefficients (b, a).
    """
    # TODO Write your code here. Below is mostly just placeholder code to get you started.
    X = ["1982", "1983"]
    y = [0, 1]
    coefficients = (0, 0)

    snomed = "15777000"
    years = []

    for _, row in df.iterrows():
        code_obj = row["code"]
        recorded = row["recordedDate"]

        if isinstance(code_obj, dict):
            codings = code_obj.get("coding", [])
            for item in codings:
                if str(item.get("code")) == snomed:
                    if isinstance(recorded, str):
                        years.append(int(recorded[:4]))
                    break

    if len(years) == 0:
        return 0.0

    year_counts = pd.Series(years).value_counts().sort_index()
    cumulative = year_counts.cumsum()

    X = cumulative.index.values.astype(float)
    y = cumulative.values.astype(float)

    coefficients = np.polyfit(X, y, 1)

    return float(coefficients[0] * year + coefficients[1])


def fhir_bulk_exporter_top3_procedures() -> Tuple[str]:
    """
    Q4. Use the SMART Bulk Data exporter (link from Canvas) to determine the top 3 procedures
    done for the patient group Health New England. You will have to export the data yourself.
    You won't have to write any code for this question. Just return the right 3 procedure names
    in order.

    Return just a tuple of the top 3 procedures in a string tuple
    eg) return ('procedure_a', 'procedure_b', 'procedure_c')

    Note: In the case of a tie, use the first result in alphabetical order. For example, if
    'aaa' and 'aab' are a tie, provide 'aaa'.

    """
    return (
        "Auscultation of the fetal heart",
        "Evaluation of uterine fundal height",
        "Medication Reconciliation (procedure)",)


def main():
    from .dataloader import get_bulk_data

    dataframe = get_bulk_data()
    q1 = count_all_prediabetes(dataframe)
    print(f"Q1: {q1}")
    q2 = count_prediabetes_timerange(dataframe, 1982, 1990)
    print(f"Q2: {q2}")
    q3 = predict_future_cumulative_prediabetes(dataframe, 2024)
    print(f"Q3: {q3}")
    q4 = fhir_bulk_exporter_top3_procedures()
    print(f"Q4: {q4}")
