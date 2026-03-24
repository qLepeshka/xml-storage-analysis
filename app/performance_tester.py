import time
import statistics
from datetime import datetime
import pandas as pd


class PerformanceTester:
    def __init__(self):
        self.test_results = []
        self.operations = ['read', 'write', 'update', 'search']

    def run_comprehensive_test(self, db_manager, storage_methods, test_config):
        results = {}

        for db_type in test_config['databases']:
            results[db_type] = {}

            for method_name in test_config['methods']:
                print(f"Тестирование {method_name} на {db_type}...")

                db_config = test_config['db_configs'][db_type]
                if db_type == 'postgresql':
                    db_manager.connect_postgresql(**db_config)
                elif db_type == 'mysql':
                    db_manager.connect_mysql(**db_config)
                elif db_type == 'sqlserver':
                    db_manager.connect_sqlserver(**db_config)

                storage_method = storage_methods.get_method(method_name)

                method_results = {}
                for operation in self.operations:
                    op_results = self._run_operation_test(
                        db_manager,
                        storage_method,
                        db_type,
                        operation,
                        test_config
                    )
                    method_results[operation] = op_results

                results[db_type][method_name] = method_results

        self.test_results = results
        return results

    def _run_operation_test(self, db_manager, storage_method, db_type, operation, test_config):
        operation_results = {
            'times': [],
            'avg_time': 0,
            'min_time': 0,
            'max_time': 0,
            'std_dev': 0
        }

        test_data = self._generate_test_data(test_config['data_size'])

        for _ in range(test_config.get('warmup_runs', 3)):
            self._execute_operation(db_manager, storage_method, db_type, operation, test_data)

        for i in range(test_config['test_runs']):
            start_time = time.time()

            try:
                result = self._execute_operation(db_manager, storage_method, db_type, operation, test_data)
                end_time = time.time()

                elapsed_time = (end_time - start_time) * 1000
                operation_results['times'].append(elapsed_time)

                if operation == 'write':
                    test_data = self._generate_test_data(test_config['data_size'])

            except Exception as e:
                print(f"Ошибка во время теста {operation}: {e}")
                operation_results['times'].append(float('inf'))

        times = [t for t in operation_results['times'] if t != float('inf')]
        if times:
            operation_results['avg_time'] = statistics.mean(times)
            operation_results['min_time'] = min(times)
            operation_results['max_time'] = max(times)
            operation_results['std_dev'] = statistics.stdev(times) if len(times) > 1 else 0
        else:
            operation_results['avg_time'] = float('inf')
            operation_results['min_time'] = float('inf')
            operation_results['max_time'] = float('inf')
            operation_results['std_dev'] = float('inf')

        return operation_results

    def _execute_operation(self, db_manager, storage_method, db_type, operation, test_data):
        engine = db_manager.engines[db_type]

        with engine.connect() as conn:
            trans = conn.begin()
            try:
                if operation == 'write':
                    table_name = f"test_{int(time.time())}_{operation}"
                    result = storage_method.store_xml(test_data, conn, table_name)
                elif operation == 'read':
                    table_name = test_data.get('table_name', 'xml_test_data')
                    result = storage_method.retrieve_xml(conn, table_name)
                elif operation == 'update':
                    table_name = test_data.get('table_name', 'xml_test_data')
                    result = None
                elif operation == 'search':
                    table_name = test_data.get('table_name', 'xml_test_data')
                    query_params = test_data.get('query_params', {})
                    result = storage_method.retrieve_xml(conn, table_name, query_params)

                trans.commit()
                return result
            except Exception as e:
                trans.rollback()
                raise e

    def _generate_test_data(self, size):
        xml_parts = ['<?xml version="1.0" encoding="UTF-8"?><root>']

        for i in range(size):
            xml_parts.append(f'<item id="{i}">')
            xml_parts.append(f'<name>Item {i}</name>')
            xml_parts.append(f'<value>{i * 10}</value>')
            xml_parts.append(f'<description>This is item number {i}</description>')
            xml_parts.append('</item>')

        xml_parts.append('</root>')
        return ''.join(xml_parts)

    def get_results_dataframe(self):
        rows = []

        if isinstance(self.test_results, list):
            return pd.DataFrame(self.test_results)

        for db_type, db_results in self.test_results.items():
            for method_name, method_results in db_results.items():
                for operation, op_result in method_results.items():
                    row = {
                        'database': db_type,
                        'method': method_name,
                        'operation': operation,
                        'avg_time_ms': op_result['avg_time'],
                        'min_time_ms': op_result['min_time'],
                        'max_time_ms': op_result['max_time'],
                        'std_dev_ms': op_result['std_dev']
                    }
                    rows.append(row)

        return pd.DataFrame(rows)

    def save_results(self, filepath):
        df = self.get_results_dataframe()
        df.to_csv(filepath, index=False)
        print(f"Результаты сохранены в {filepath}")
