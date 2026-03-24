import psycopg2
import pymysql
import pyodbc
from sqlalchemy import create_engine
import xml.etree.ElementTree as ET


class DatabaseManager:
    def __init__(self):
        self.connections = {}
        self.engines = {}

    def connect_postgresql(self, host, port, database, username, password):
        try:
            conn_str = f"postgresql://{username}:{password}@{host}:{port}/{database}"
            engine = create_engine(conn_str)
            self.engines['postgresql'] = engine
            print(f"Подключено к PostgreSQL: {database}")
            return True
        except Exception as e:
            print(f"Ошибка подключения к PostgreSQL: {e}")
            return False

    def connect_mysql(self, host, port, database, username, password):
        try:
            conn_str = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
            engine = create_engine(conn_str)
            self.engines['mysql'] = engine
            print(f"Подключено к MySQL: {database}")
            return True
        except Exception as e:
            print(f"Ошибка подключения к MySQL: {e}")
            return False

    def connect_sqlserver(self, host, port, database, username, password):
        try:
            conn_str = f"mssql+pyodbc://{username}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
            engine = create_engine(conn_str)
            self.engines['sqlserver'] = engine
            print(f"Подключено к SQL Server: {database}")
            return True
        except Exception as e:
            print(f"Ошибка подключения к SQL Server: {e}")
            return False

    def execute_query(self, db_type, query, params=None):
        if db_type not in self.engines:
            raise ValueError(f"Нет подключения для {db_type}")

        engine = self.engines[db_type]
        with engine.connect() as conn:
            if params:
                result = conn.execute(query, params)
            else:
                result = conn.execute(query)
            return result.fetchall()

    def create_table(self, db_type, table_name, schema):
        if db_type not in self.engines:
            raise ValueError(f"Нет подключения для {db_type}")

        engine = self.engines[db_type]
        with engine.connect() as conn:
            conn.execute(schema)
            conn.commit()

    def insert_data(self, db_type, table_name, data):
        if db_type not in self.engines:
            raise ValueError(f"Нет подключения для {db_type}")

        engine = self.engines[db_type]
        with engine.connect() as conn:
            if db_type == 'postgresql':
                placeholders = ', '.join([f'%({key})s' for key in data.keys()])
            elif db_type == 'mysql':
                placeholders = ', '.join([f'%({key})s' for key in data.keys()])
            elif db_type == 'sqlserver':
                placeholders = ', '.join([f':{key}' for key in data.keys()])

            columns = ', '.join(data.keys())
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            conn.execute(query, data)
            conn.commit()

    def close_all_connections(self):
        for engine in self.engines.values():
            engine.dispose()
