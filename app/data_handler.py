import json
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path


class DataHandler:
    def __init__(self):
        self.supported_formats = ['xml', 'json', 'csv', 'xlsx']

    def import_dataset(self, filepath, format_type=None):
        path = Path(filepath)

        if format_type is None:
            format_type = path.suffix[1:].lower()

        if format_type not in self.supported_formats:
            raise ValueError(f"Неподдерживаемый формат: {format_type}. Поддерживаемые форматы: {self.supported_formats}")

        if format_type == 'xml':
            return self._import_xml(filepath)
        elif format_type == 'json':
            return self._import_json(filepath)
        elif format_type == 'csv':
            return self._import_csv(filepath)
        elif format_type == 'xlsx':
            return self._import_excel(filepath)

    def export_dataset(self, data, filepath, format_type=None):
        path = Path(filepath)

        if format_type is None:
            format_type = path.suffix[1:].lower()

        if format_type not in self.supported_formats:
            raise ValueError(f"Неподдерживаемый формат: {format_type}. Поддерживаемые форматы: {self.supported_formats}")

        if format_type == 'xml':
            return self._export_xml(data, filepath)
        elif format_type == 'json':
            return self._export_json(data, filepath)
        elif format_type == 'csv':
            return self._export_csv(data, filepath)
        elif format_type == 'xlsx':
            return self._export_excel(data, filepath)

    def _import_xml(self, filepath):
        tree = ET.parse(filepath)
        root = tree.getroot()
        return ET.tostring(root, encoding='unicode')

    def _import_json(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _import_csv(self, filepath):
        df = pd.read_csv(filepath)
        return df.to_dict('records')

    def _import_excel(self, filepath):
        df = pd.read_excel(filepath)
        return df.to_dict('records')

    def _export_xml(self, data, filepath):
        if isinstance(data, str):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(data)
        else:
            root = ET.Element("root")
            self._dict_to_xml(data, root)
            tree = ET.ElementTree(root)
            tree.write(filepath, encoding='unicode', xml_declaration=True)

    def _dict_to_xml(self, data, parent):
        if isinstance(data, dict):
            for key, value in data.items():
                elem = ET.SubElement(parent, key)
                self._dict_to_xml(value, elem)
        elif isinstance(data, list):
            for item in data:
                elem = ET.SubElement(parent, "item")
                self._dict_to_xml(item, elem)
        else:
            parent.text = str(data)

    def _export_json(self, data, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _export_csv(self, data, filepath):
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame([data]) if not isinstance(data, list) else pd.DataFrame(data)

        df.to_csv(filepath, index=False)

    def _export_excel(self, data, filepath):
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame([data]) if not isinstance(data, list) else pd.DataFrame(data)

        df.to_excel(filepath, index=False)

    def validate_xml(self, xml_string):
        try:
            ET.fromstring(xml_string)
            return True
        except ET.ParseError:
            return False

    def generate_sample_xml(self, size=10):
        root = ET.Element("sample_data")

        for i in range(size):
            item = ET.SubElement(root, "item")
            item.set("id", str(i))

            name = ET.SubElement(item, "name")
            name.text = f"Item {i}"

            value = ET.SubElement(item, "value")
            value.text = str(i * 10)

            description = ET.SubElement(item, "description")
            description.text = f"This is item number {i} with some sample content."

        return ET.tostring(root, encoding='unicode')
