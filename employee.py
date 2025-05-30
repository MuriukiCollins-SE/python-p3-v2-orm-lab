from db import CONN, CURSOR
from department import Department

class Employee:
    all = {}

    def __init__(self, name, job_title, department_id, id=None):
        self.id = id
        self.name = name
        self._job_title = job_title
        self._department_id = department_id
        if id is not None:
            Employee.all[id] = self

    @classmethod
    def create_table(cls):
        """Create a employees table if it does not exist."""
        Department.create_table()
        sql = """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                department_id INTEGER NOT NULL,
                FOREIGN KEY (department_id) REFERENCES departments(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        # Drop reviews first to avoid FK constraint error, then employees
        try:
            CURSOR.execute("DROP TABLE IF EXISTS reviews")
        except Exception:
            pass
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CONN.commit()
        cls.all.clear()

    def save(self):
        """Save the Employee instance to the database and assign an ID."""
        # Validate department_id before saving to avoid FK constraint errors
        if not isinstance(self.department_id, int):
            raise ValueError("Department ID must be an integer")
        sql = "SELECT id FROM departments WHERE id = ?"
        result = CURSOR.execute(sql, (self.department_id,)).fetchone()
        if not result:
            raise ValueError("Department ID must reference an existing department")
        if self.id:
            self.update()
        else:
            sql = """
                INSERT INTO employees (name, job_title, department_id)
                VALUES (?, ?, ?)
            """
            CURSOR.execute(sql, (self.name, self.job_title, self.department_id))
            CONN.commit()
            self.id = CURSOR.lastrowid
            Employee.all[self.id] = self

    @classmethod
    def create(cls, name, job_title, department_id):
        """Create a new employee in the database and return the instance."""
        employee = cls(name, job_title, department_id)
        employee.save()
        return employee

    @classmethod
    def instance_from_db(cls, row):
        """Create an Employee instance from a database row."""
        if row:
            id, name, job_title, department_id = row
            if id in cls.all:
                return cls.all[id]
            return cls(name, job_title, department_id, id)
        return None

    @classmethod
    def find_by_id(cls, id):
        """Find an Employee instance by ID."""
        sql = "SELECT * FROM employees WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row)

    @classmethod
    def find_by_name(cls, name):
        """Find an Employee instance by name."""
        sql = "SELECT * FROM employees WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row)

    def update(self):
        """Update the employee's database row."""
        sql = """
            UPDATE employees
            SET name = ?, job_title = ?, department_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.job_title, self.department_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the employee's database row."""
        sql = "DELETE FROM employees WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        Employee.all.pop(self.id, None)
        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list of all Employee instances."""
        sql = "SELECT * FROM employees"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def reviews(self):
        """Return a list of Review instances for this employee."""
        from review import Review  # Avoid circular import
        sql = "SELECT * FROM reviews WHERE employee_id = ?"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Review.instance_from_db(row) for row in rows]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def job_title(self):
        return self._job_title

    @job_title.setter
    def job_title(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Job title must be a non-empty string")
        self._job_title = value

    @property
    def department_id(self):
        return self._department_id

    @department_id.setter
    def department_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Department ID must be an integer")
        sql = "SELECT id FROM departments WHERE id = ?"
        result = CURSOR.execute(sql, (value,)).fetchone()
        if not result:
            raise ValueError("Department ID must reference an existing department")
        self._department_id = value