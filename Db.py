import mysql.connector as sql
from django.conf import settings

DATABASES = settings.DATABASES

_connection = None

def get_connection():
    global _connection
    if _connection is None:
        _connection = sql.connect(
            host=DATABASES["default"]["HOST"],
            user=DATABASES["default"]["USER"],
            password=DATABASES["default"]["PASSWORD"],
            database=DATABASES["default"]["NAME"],
            auth_plugin='mysql_native_password',
            connect_timeout=100
        )
        _connection.autocommit = True
    return _connection

def closeConnection():
    global _connection
    if _connection:
        _connection.close()
    _connection = None
