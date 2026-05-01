from util.OmopOnFhir import t_measurement, t_f_person

### Introduction
"""
All student code that is submitted to Gradescope will be written in this file. It is divided into
two sections: "Questions" and "Data Model Exercises". For the Questions section, simply return what
is being asked as a string. This will require some exploration of the database. The functions exist
in isolation with no input, and you will be expected to hardcode everything according to what is being
requested. For the data model exercises, you will write code that you then execute from main.py in
order to pass in inputs. (You may also execute your code through Pytest if you prefer.) For these exercises,
simple unit tests will provided. These unit tests will help confirm basic functionality. The Gradescope
autograder will consists of these simple tests as well as additional hidden tests.

WARNING: Do not connect to a database in this file. All inputs to student functions defined here
should be a representation of a table row or rows in the format of the provided SQL Alchemy models,
which are in the form of tuples. (Tuples are a sequence of comma separated data wrapped in basic
parenthesis.) Each element in the tuple matches to the column order defined in the appropriate table from the
utils/OmopOnFhir.py file.

For example, the t_measurement model represents the Measurement table. Per the schema model
provided, for a given tuple represeting a row from the measurement table, the person_id is going to
be accessed through row[1]. You can also get the name of the column via the same index access at
t_measurement.c[n], though we will not ask you to return this it is helpful for a reference.
For example:

>>> print(t_measurement.c[8], t_measurement_row[8])
measurement.value_as_number 6.2
"""

### Questions
"""
QUESTION 1:
After posting patient_1.json to the OMOPonFHIR it will be written to the OMOP database. If you
then read the patient back from the FHIR server, additional data may be added as part of
standardized representation. For example, the U.S. Core Race element is not present on in the
patient_1.json file, but it will be generated when the resource is requested. What is the *code*
returned for the US Core Race's coding in this case? (Case Sensitive!)
"""


def question_1():
    answer: str = "UNK"  # Set your answer here.
    return answer


"""
QUESTION 2:
Three Observation resources are given, observation_1.json through observation_3.json. FHIR Observations
line up with two different tables based on how it is categorized in the concept tables from the loaded
vocabulary. Post all three to the OMOPonFHIR Server. Which of the two OMOP CDM tables does each get stored
in? (Case Sensitive! Use all lower case.)
"""


def question_2_observation_1():
    answer: str = "measurement"  # Set your answer here.
    return answer


def question_2_observation_2():
    answer: str = "measurement"  # Set your answer here.
    return answer


def question_2_observation_3():
    answer: str = "observation"  # Set your answer here.
    return answer


"""
QUESTION 3:
Now, post observation_4.json to the FHIR Server. This file gets written to the observation table. Due
to complexities in mapping, the valueCodeableConcept field in the original FHIR resource is replaced
with what field when requested back from the server? (Answer with the full string for the field key,
exactly as it is given. Case Sensitive!)
"""


def question_3():
    answer: str = "valueString"  # Set your answer here.
    return answer


"""
QUESTION 4:
Moving to the two MedicationStatement resources, post both to the FHIR Server if you have not. What
OMOP CDM table are they populated into? (Case Sensitive! Use all lowercase.)
"""


def question_4():
    answer: str = "drug_exposure"  # Set your answer here.
    return answer


### Data Model Exercises
"""
# Exercise 1 - Get Measurement Value
Return the value of an entry in the Measurement table. Consider only the value_as_number data type.

## INPUT
A single line from the Measurement table, given as a tuple.

### Example
(2, 1, 3013290, datetime.date(2013, 4, 2), datetime.datetime(2013, 4, 2, 9, 30, 10), None, 0, None, Decimal('6.2'), None, 44777602, Decimal('4.8'), Decimal('6.0'), None, None, None, None, 3013290, 'kPa', None, '6.2', None, None)

## OUTPUT
A number as a float or None if no value exists.
- Note 1: The "Decimal" type has a higher percision than a float, but for simplicity given the data we are working with we will
  stick to floats. As the model provided uses Decimal, you will need to wrap your response in float(your_answer) before returning
  or it will fail tests.

### Example
6.2
None
"""


def get_measurement_value(t_measurement_row):
    value = t_measurement_row[8]
    if value is None:
        return None
    return float(value)


"""
# Exercise 2 - Get Patient Full Name
Return the full name (first given name and family/last name) of a person from the OMOP on FHIR F_Person table.

## INPUT
A single row from the f_person table, given as a tuple in alignment with the provided database models.

## OUTPUT
A string that combines the patient's *first* given name and their family name with a space between them.

Example:
"John Doe"
"""


def get_patient_name(t_f_person_row):
    given = t_f_person_row[2]
    family = t_f_person_row[1]
    return f"{given} {family}"


"""
# Exercise 3 - Get Patient Gender as String
Return the string representation of a patient's gender (e.g. "male", "female", "other", "unknown").

## INPUT
A row from a JOIN of the person table and a second table which contains the requested value. The name of
the second table and column are not given here on purpose, you must determine what these are through the
documentation. For this test, do not assume a consistent input tuple. Columns from the two tables may
appear in any order. You must access the field via the column name. To do this, you can use the provided
get_column_index function which returns the index of the column in question.

## OUTPUT
The patient's gender as a string.

Example:
"MALE"
"""


def get_patient_gender_as_string(joined_row, keys):
    idx = get_column_index("concept_name", keys)
    return joined_row[idx]


# Helper function for getting the index of a given column dynamically.
def get_column_index(column_name: str, keys):
    idx = [idx for (idx, i) in enumerate(keys) if i == column_name][0]
    return idx
