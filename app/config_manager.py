import json
import yaml
from pathlib import Path


class ConfigManager:
    def __init__(self, config_file=None):
        self.config = self._get_default_config()

        if config_file:
            self.load_config(config_file)

    def _get_default_config(self):
        return {
            "databases": ["postgresql", "mysql", "sqlserver"],
            "methods": [
                "native_text",
                "normalized_relational",
                "xml_datatype",
                "hybrid"
            ],
            "operations": ["read", "write", "update", "search"],
            "test_parameters": {
                "data_size": 100,
                "test_runs": 10,
                "warmup_runs": 3,
                "timeout": 30
            },
            "database_configs": {
                "postgresql": {
                    "host": "localhost",
                    "port": 5432,
                    "database": "xml_test",
                    "username": "postgres",
                    "password": "password"
                },
                "mysql": {
                    "host": "localhost",
                    "port": 3306,
                    "database": "xml_test",
                    "username": "root",
                    "password": "password"
                },
                "sqlserver": {
                    "host": "localhost",
                    "port": 1433,
                    "database": "xml_test",
                    "username": "sa",
                    "password": "Password123!"
                }
            },
            "output_settings": {
                "results_file": "results/test_results.csv",
                "report_dir": "reports/",
                "visualization_dir": "visualizations/"
            }
        }

    def load_config(self, config_file):
        path = Path(config_file)

        if not path.exists():
            raise FileNotFoundError(f"Файл конфигурации не найден: {config_file}")

        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix.lower() in ['.yaml', '.yml']:
                file_config = yaml.safe_load(f)
            elif path.suffix.lower() == '.json':
                file_config = json.load(f)
            else:
                raise ValueError(f"Неподдерживаемый формат файла конфигурации: {path.suffix}")

        self.config = self._merge_configs(self.config, file_config)

    def save_config(self, config_file):
        path = Path(config_file)

        with open(path, 'w', encoding='utf-8') as f:
            if path.suffix.lower() in ['.yaml', '.yml']:
                yaml.dump(self.config, f, default_flow_style=False)
            elif path.suffix.lower() == '.json':
                json.dump(self.config, f, indent=2)
            else:
                raise ValueError(f"Неподдерживаемый формат файла конфигурации: {path.suffix}")

    def _merge_configs(self, default_config, override_config):
        result = default_config.copy()

        for key, value in override_config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key, value):
        keys = key.split('.')
        config_ref = self.config

        for k in keys[:-1]:
            if k not in config_ref or not isinstance(config_ref[k], dict):
                config_ref[k] = {}
            config_ref = config_ref[k]

        config_ref[keys[-1]] = value

    def get_database_config(self, db_type):
        return self.config['database_configs'].get(db_type, {})

    def get_test_parameters(self):
        return self.config['test_parameters']

    def get_output_settings(self):
        return self.config['output_settings']

    def validate_config(self):
        errors = []

        for db_type in self.config['databases']:
            if db_type not in self.config['database_configs']:
                errors.append(f"Отсутствует конфигурация для базы данных: {db_type}")

        available_methods = [
            "native_text",
            "normalized_relational",
            "xml_datatype",
            "hybrid"
        ]
        for method in self.config['methods']:
            if method not in available_methods:
                errors.append(f"Неизвестный метод хранения: {method}")

        available_operations = ["read", "write", "update", "search"]
        for operation in self.config['operations']:
            if operation not in available_operations:
                errors.append(f"Неизвестная операция: {operation}")

        return errors
