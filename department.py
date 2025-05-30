from db import CONN, CURSOR

class Department:
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location
        if id is not None:
            Department.all[id] = self

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                location TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        CONN.commit()
        cls.all.clear()

    def save(self):
        if self.id:
            self.update()
        else:
            sql = """
                INSERT INTO departments (name, location)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.location))
            CONN.commit()
            self.id = CURSOR.lastrowid
            Department.all[self.id] = self

    @classmethod
    def create(cls, name, location):
        department = cls(name, location)
        department.save()
        return department

    @classmethod
    def instance_from_db(cls, row):
        if row:
            id, name, location = row
            if id in cls.all:
                return cls.all[id]
            department = cls(name, location, id)
            return department
        return None

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM departments WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row)

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM departments WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row)

    def update(self):
        """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        sql = CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the department's database row."""
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        # Remove from all dictionaries and set id to None
        Department.all.pop(self.id, None)
        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list of all Department instances."""
        sql = "SELECT * FROM departments"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def employees(self):
        """Return a list of Employee instances for this department."""
        from employee import Employee  # Avoid circular import
        sql = "SELECT * FROM employees WHERE department_id = ?"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Employee.instance_from_db(row) for row in rows]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def location(self):
        return self._location


    @location.setter
    def location(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Location must be a non-empty string")
        self._location = value