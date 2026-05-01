from util.sqlalchemydb import create_connection
from util.OmopOnFhir import t_f_person, t_measurement, t_person
from sqlalchemy.orm import Session
from sqlalchemy import text, select

from student_code import get_measurement_value, get_patient_name, get_patient_gender_as_string

# Modify your database connection string as needed.
database_connection_string: str = "postgresql://postgres:password@localhost:5432/omop54"

def main():
    engine = create_connection(database_connection_string, True)
    call_exercise_1_using_sql_example(engine)
    #call_exercise_2(engine)
    #call_exercise_3(engine)

'''
Two examples are provided below, the first using a standard SQL statement. The second using the SQL
Alchemy models more directly. Either approach may be used.
'''
def call_exercise_1_using_sql_example(engine):
    with Session(engine) as session:
        statement = f'SELECT * FROM measurement;'
        result = session.execute(text(statement))
        for row in result.all():
           print(get_measurement_value(row))


def call_exercise_1_using_sqlalchemy(engine):
    with Session(engine) as session:
        statement = select(t_measurement)
        result = session.execute(statement)
        for row in result.all():
           print(get_measurement_value(row))


def call_exercise_2(engine):
    with Session(engine) as session:
        statement = select(t_f_person)
        result = session.execute(statement)
        for row in result.all():
            print(get_patient_name(row))

'''
The following exercise requires performing a JOIN on two tables, which will align the tables along a single column. To make this
easier for those who are not familiar with SQL, the bulk of the SQL statement is given for you. You should only need to edit the variables
at the top of the function in alignment with the OMOP CDM schema.

An example of a full JOIN statement performed on the person and f_person tables:
>>> SELECT * FROM person INNER JOIN f_person ON person.person_id=f_person.person_id;

Note additionally the inclusion of the "result.keys()" usage. This allows you to access the column descriptions from the query itself,
not using the local models provided. For this particular case, as a JOIN can produce any number of columns in any order, pulling this
from the result will help align the data with the request more directly. It will be used in the exercise_3 function to dynamically
determine the index of the column requested. Please read the description given in the student_code.py file for more information before
writing any code here.
'''
def call_exercise_3(engine):
    columns = "*"               # The columns you wish return. You can leave this as * if you would like.
    second_table = ""           # The name of the second table.
    foreign_key = ""            # The name of the foreign key in the person table on which to join with the second table.
    foreign_key_equivalent = "" # The name of the column in the second table which lines up with the person table's foreign key.

    with Session(engine) as session:
        statement = f'SELECT {columns} FROM person INNER JOIN {second_table} ON person.{foreign_key}={second_table}.{foreign_key_equivalent} LIMIT 10;'
        result = session.execute(text(statement))
        keys = result.keys()
        for row in result.all():
            print(get_patient_gender_as_string(row, keys))


if __name__ == '__main__':
    main()
