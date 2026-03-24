import xml.etree.ElementTree as ET
import json
from abc import ABC, abstractmethod


class StorageMethod(ABC):
    @abstractmethod
    def store_xml(self, xml_data, connection, table_name):
        pass

    @abstractmethod
    def retrieve_xml(self, connection, table_name, query_params=None):
        pass


class NativeTextStorage(StorageMethod):
    def store_xml(self, xml_data, connection, table_name):
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            xml_content TEXT
        )
        """
        connection.execute(create_table_sql)

        insert_sql = f"INSERT INTO {table_name} (xml_content) VALUES (%s)"
        connection.execute(insert_sql, (xml_data,))

        return connection.lastrowid

    def retrieve_xml(self, connection, table_name, query_params=None):
        select_sql = f"SELECT xml_content FROM {table_name}"
        if query_params:
            select_sql += " WHERE " + " AND ".join([f"{k}=%s" for k in query_params.keys()])
            connection.execute(select_sql, list(query_params.values()))
        else:
            connection.execute(select_sql)

        results = connection.fetchall()
        return [row[0] for row in results]


class NormalizedRelationalStorage(StorageMethod):
    def __init__(self):
        self.schema_cache = {}

    def _generate_schema_from_xml(self, xml_data):
        root = ET.fromstring(xml_data)
        schema = {}

        def parse_element(element, path=""):
            current_path = f"{path}/{element.tag}" if path else element.tag

            for attr_name, attr_value in element.attrib.items():
                schema[f"{current_path}/@{attr_name}"] = "TEXT"

            if element.text and element.text.strip():
                schema[current_path] = "TEXT"

            for child in element:
                parse_element(child, current_path)

        parse_element(root)
        return schema

    def store_xml(self, xml_data, connection, table_name):
        root = ET.fromstring(xml_data)

        if table_name not in self.schema_cache:
            self.schema_cache[table_name] = self._generate_schema_from_xml(xml_data)

        columns = []
        for field_name, field_type in self.schema_cache[table_name].items():
            safe_field_name = field_name.replace("/", "_").replace("@", "attr_")
            columns.append(f"{safe_field_name} {field_type}")

        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            {', '.join(columns)}
        )
        """
        connection.execute(create_table_sql)

        values = {}
        def extract_values(element, path=""):
            current_path = f"{path}/{element.tag}" if path else element.tag

            for attr_name, attr_value in element.attrib.items():
                safe_key = f"{current_path}/@{attr_name}".replace("/", "_").replace("@", "attr_")
                values[safe_key] = attr_value

            if element.text and element.text.strip():
                safe_key = current_path.replace("/", "_").replace("@", "attr_")
                values[safe_key] = element.text

            for child in element:
                extract_values(child, current_path)

        extract_values(root)

        columns_list = list(values.keys())
        placeholders = ", ".join([f"%({col})s" for col in columns_list])
        columns_str = ", ".join(columns_list)

        insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        connection.execute(insert_sql, values)

        return connection.lastrowid

    def retrieve_xml(self, connection, table_name, query_params=None):
        select_sql = f"SELECT * FROM {table_name}"
        if query_params:
            select_sql += " WHERE " + " AND ".join([f"{k}=%s" for k in query_params.keys()])
            connection.execute(select_sql, list(query_params.values()))
        else:
            connection.execute(select_sql)

        rows = connection.fetchall()
        column_names = [desc[0] for desc in connection.description]

        results = []
        for row in rows:
            row_dict = dict(zip(column_names, row))
            results.append(json.dumps(row_dict))

        return results


class XMLDataTypeStorage(StorageMethod):
    def store_xml(self, xml_data, connection, table_name):
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            xml_content XML
        )
        """
        connection.execute(create_table_sql)

        insert_sql = f"INSERT INTO {table_name} (xml_content) VALUES (%s)"
        connection.execute(insert_sql, (xml_data,))

        return connection.lastrowid

    def retrieve_xml(self, connection, table_name, query_params=None):
        select_sql = f"SELECT xml_content FROM {table_name}"
        if query_params:
            select_sql += " WHERE " + " AND ".join([f"{k}=%s" for k in query_params.keys()])
            connection.execute(select_sql, list(query_params.values()))
        else:
            connection.execute(select_sql)

        results = connection.fetchall()
        return [row[0] for row in results]


class HybridStorage(StorageMethod):
    def __init__(self):
        self.native_storage = NativeTextStorage()
        self.relational_storage = NormalizedRelationalStorage()

    def store_xml(self, xml_data, connection, table_name):
        native_id = self.native_storage.store_xml(xml_data, connection, f"{table_name}_native")
        relational_id = self.relational_storage.store_xml(xml_data, connection, f"{table_name}_relational")

        create_mapping_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name}_mapping (
            id SERIAL PRIMARY KEY,
            native_id INTEGER,
            relational_id INTEGER
        )
        """
        connection.execute(create_mapping_sql)

        insert_mapping_sql = f"INSERT INTO {table_name}_mapping (native_id, relational_id) VALUES (%s, %s)"
        connection.execute(insert_mapping_sql, (native_id, relational_id))

        return native_id, relational_id

    def retrieve_xml(self, connection, table_name, query_params=None):
        return self.native_storage.retrieve_xml(connection, f"{table_name}_native", query_params)


class StorageMethods:
    def __init__(self):
        self.methods = {
            'native_text': NativeTextStorage(),
            'normalized_relational': NormalizedRelationalStorage(),
            'xml_datatype': XMLDataTypeStorage(),
            'hybrid': HybridStorage()
        }

    def get_method(self, method_name):
        if method_name in self.methods:
            return self.methods[method_name]
        else:
            raise ValueError(f"Неизвестный метод хранения: {method_name}")

    def list_methods(self):
        return list(self.methods.keys())
