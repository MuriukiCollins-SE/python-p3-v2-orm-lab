from db import CONN, CURSOR
from department import Department
from employee import Employee
from review import Review
import pytest

class TestDepartment:
    '''Class Department in department.py'''

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