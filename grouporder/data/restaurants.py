import psycopg2
from flask import g
from psycopg2 import errorcodes


class DuplicateRestaurantNameError(RuntimeError):
    pass


class Restaurant:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        query = """
        INSERT INTO
          restaurants
          (name)
        VALUES
          (%s)
        RETURNING
          restaurant_id;
        """

        with g.db.cursor() as cursor:
            try:
                cursor.execute(query, (name,))
                g.db.commit()
                id = cursor.fetchone()[0]
                return cls(id=id, name=name)
            except psycopg2.Error as e:
                if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                    raise DuplicateRestaurantNameError()

    @classmethod
    def by_id(cls, id):
        query = """
        SELECT restaurant_id, name FROM restaurants WHERE restaurant_id = %s;
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (id,))
            row = cursor.fetchone()

        return cls(id=row[0], name=row[1])

    def rename(self, name):
        query = """
        UPDATE
            restaurants
        SET
          name = %s
        WHERE
          restaurant_id = %s;
        """

        with g.db.cursor() as cursor:
            try:
                cursor.execute(query, (name, self.id))
                g.db.commit()
            except psycopg2.Error as e:
                if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                    raise DuplicateRestaurantNameError()

    @classmethod
    def list(cls):
        query = """
            SELECT restaurant_id, name FROM restaurants;
        """

        with g.db.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        restaurants = []
        for row in rows:
            restaurant = cls(id=row[0], name=row[1])
            restaurants.append(restaurant)

        return restaurants
