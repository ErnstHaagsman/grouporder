import psycopg2
from flask import g
from psycopg2 import errorcodes
from passlib.hash import bcrypt

class DuplicateUserError(RuntimeError):
    pass


def _crypt_password(password):
    return bcrypt.using(rounds=12).hash(password)

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

    @classmethod
    def create(cls,
               username,
               fullname,
               email,
               password,
               can_manage_restaurants=False):

        password_hash = _crypt_password(password)

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

    @classmethod
    def from_token(cls, token):
        """
        Takes a session token, and returns a user object if the token is valid
        or None if the token is invalid.
        """

        query = """
            SELECT 
              u.username, fullname, email, can_manage_restaurants
            FROM
              users u
            INNER JOIN
              sessions s on u.username = s.username
            WHERE
              s.token = %s and s.expiration > now();
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (token,))
            session = cursor.fetchone()

        if session is None:
            return None

        return cls(username=session[0],
                   fullname=session[1],
                   email=session[2],
                   can_manage_restaurants=session[3])


def login(username, password):
    """
    Attempt to log in a user, returns a session string if successful,
    or None if unsuccessful
    """

    query = """
        SELECT password FROM users WHERE
          username = %s;
    """

    with g.db.cursor() as cursor:
        cursor.execute(query, (username,))
        password_row = cursor.fetchone()

    if password_row is None or not bcrypt.verify(password, password_row[0]):
        return None

    session_query = """
        INSERT INTO sessions
          (token, username, expiration) 
        VALUES 
          (gen_random_uuid(), %s, now() + interval '3 hours')
        RETURNING
          token;
    """

    with g.db.cursor() as cursor:
        cursor.execute(session_query, (username,))
        token = cursor.fetchone()[0]

    g.db.commit()

    return token