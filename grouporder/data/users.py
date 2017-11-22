import psycopg2
from flask import g
from psycopg2 import errorcodes
from passlib.hash import bcrypt

class DuplicateUserError(RuntimeError):
    pass

class User():
    def __init__(self,
                 username=None,
                 fullname=None,
                 email=None,
                 can_manage_restaurants=False):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.can_manage_restaurants = can_manage_restaurants

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'fullname': self.fullname
        }

    @classmethod
    def create(cls,
               username,
               fullname,
               email,
               password,
               can_manage_restaurants=False):

        password_hash = bcrypt.using(rounds=12).hash(password)

        query = """
            INSERT INTO users
              (username, fullname, password, email, can_manage_restaurants)
            VALUES 
              (%s, %s, %s, %s, %s);
        """

        with g.db.cursor() as cursor:
            try:
                cursor.execute(query,
                           (username, fullname, password_hash, email,
                            can_manage_restaurants))

                g.db.commit()
            except psycopg2.Error as e:
                if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                    raise DuplicateUserError('Username already exists')

        return cls(username, fullname, email, can_manage_restaurants)
