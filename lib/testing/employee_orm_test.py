from db import CONN, CURSOR
from employee import Employee
from department import Department
from review import Review
from faker import Faker
import pytest

class TestEmployee:
    '''Class Employee in employee.py'''

    @pytest.fixture(autouse=True)
    def reset_db(self):
        CURSOR.execute("DROP TABLE IF EXISTS reviews")
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        CONN.commit()
        Department.all.clear()
        Employee.all.clear()
        Review.all.clear()
        Department.create_table()
        Employee.create_table()
        Review.create_table()

    # Existing test methods...