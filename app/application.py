import argparse
from app.database_manager import DatabaseManager
from app.storage_methods import StorageMethods
from app.performance_tester import PerformanceTester
from app.visualizer import Visualizer
from app.report_generator import ReportGenerator
from app.data_handler import DataHandler
from app.config_manager import ConfigManager


class Application:
    def __init__(self, config_file=None):
        self.config_manager = ConfigManager(config_file)
        self.db_manager = DatabaseManager()
        self.storage_methods = StorageMethods()
        self.performance_tester = PerformanceTester()
        self.visualizer = Visualizer()
        self.report_generator = ReportGenerator()
        self.data_handler = DataHandler()

    def run(self):
        parser = argparse.ArgumentParser(description='Инструмент сравнительного анализа методов хранения XML')
        parser.add_argument('--config', type=str, help='Путь к файлу конфигурации')
        parser.add_argument('--action', type=str, choices=['test', 'visualize', 'report', 'import', 'export'],
                           help='Действие для выполнения')

        args = parser.parse_args()

        config_file = args.config

        if config_file:
            self.config_manager.load_config(config_file)

        validation_errors = self.config_manager.validate_config()
        if validation_errors:
            print("Обнаружены ошибки конфигурации:")
            for error in validation_errors:
                print(f"  - {error}")
            return

        if args.action == 'test':
            self.run_performance_tests()
        elif args.action == 'visualize':
            self.generate_visualizations()
        elif args.action == 'report':
            self.generate_report()
        elif args.action == 'import':
            self.import_dataset()
        elif args.action == 'export':
            self.export_dataset()
        else:
            self.show_menu()

    def show_menu(self):
        print("Инструмент сравнительного анализа методов хранения XML")
        print("=" * 50)
        print("1. Настройка баз данных")
        print("2. Запуск тестов производительности")
        print("3. Генерация визуализаций")
        print("4. Генерация отчёта")
        print("5. Импорт набора данных")
        print("6. Экспорт набора данных")
        print("7. Выход")

        choice = input("\nВведите ваш выбор: ")

        if choice == '1':
            self.configure_databases()
        elif choice == '2':
            self.run_performance_tests()
        elif choice == '3':
            self.generate_visualizations()
        elif choice == '4':
            self.generate_report()
        elif choice == '5':
            self.import_dataset()
        elif choice == '6':
            self.export_dataset()
        elif choice == '7':
            exit(0)
        else:
            print("Неверный выбор. Попробуйте снова.")
            self.show_menu()

    def configure_databases(self):
        print("Настройка баз данных...")
        pass

    def run_performance_tests(self):
        print("Запуск тестов производительности...")

        test_config = {
            'databases': self.config_manager.get('databases'),
            'methods': self.config_manager.get('methods'),
            'operations': self.config_manager.get('operations'),
            'db_configs': self.config_manager.get('database_configs'),
        }
        test_config.update(self.config_manager.get('test_parameters'))

        results = self.performance_tester.run_comprehensive_test(
            self.db_manager,
            self.storage_methods,
            test_config
        )

        results_file = self.config_manager.get('output_settings.results_file')
        self.performance_tester.save_results(results_file)

        print(f"Тесты производительности завершены. Результаты сохранены в {results_file}")
        return results

    def generate_visualizations(self):
        print("Генерация визуализаций...")

        df = self.performance_tester.get_results_dataframe()

        if df.empty:
            print("Нет результатов тестов. Сначала запустите тесты производительности.")
            print("Загрузка тестовых данных для демонстрации...")
            df = self._load_demo_data()

        visualizations = self.visualizer.generate_all_visualizations(df)

        viz_dir = self.config_manager.get('output_settings.visualization_dir')
        import os
        try:
            os.makedirs(viz_dir, exist_ok=True)
        except FileExistsError:
            pass

        for name, fig in visualizations.items():
            filepath = os.path.join(viz_dir, f"{name}.html")
            self.visualizer.save_visualization(fig, filepath)

        print(f"Визуализации сгенерированы и сохранены в {viz_dir}")
        return visualizations

    def _load_demo_data(self):
        import pandas as pd
        demo_data = [
            {'database': 'postgresql', 'method': 'native_text', 'operation': 'read', 'avg_time_ms': 12.5, 'min_time_ms': 10.2, 'max_time_ms': 15.3, 'std_dev_ms': 1.2},
            {'database': 'postgresql', 'method': 'native_text', 'operation': 'write', 'avg_time_ms': 25.3, 'min_time_ms': 22.1, 'max_time_ms': 28.9, 'std_dev_ms': 2.1},
            {'database': 'postgresql', 'method': 'native_text', 'operation': 'update', 'avg_time_ms': 18.7, 'min_time_ms': 16.4, 'max_time_ms': 21.2, 'std_dev_ms': 1.5},
            {'database': 'postgresql', 'method': 'native_text', 'operation': 'search', 'avg_time_ms': 45.2, 'min_time_ms': 40.1, 'max_time_ms': 52.3, 'std_dev_ms': 3.8},
            {'database': 'postgresql', 'method': 'normalized_relational', 'operation': 'read', 'avg_time_ms': 8.3, 'min_time_ms': 7.1, 'max_time_ms': 9.8, 'std_dev_ms': 0.8},
            {'database': 'postgresql', 'method': 'normalized_relational', 'operation': 'write', 'avg_time_ms': 35.6, 'min_time_ms': 32.4, 'max_time_ms': 39.2, 'std_dev_ms': 2.5},
            {'database': 'postgresql', 'method': 'normalized_relational', 'operation': 'update', 'avg_time_ms': 22.1, 'min_time_ms': 19.8, 'max_time_ms': 25.3, 'std_dev_ms': 1.8},
            {'database': 'postgresql', 'method': 'normalized_relational', 'operation': 'search', 'avg_time_ms': 15.4, 'min_time_ms': 13.2, 'max_time_ms': 18.1, 'std_dev_ms': 1.3},
            {'database': 'postgresql', 'method': 'xml_datatype', 'operation': 'read', 'avg_time_ms': 10.1, 'min_time_ms': 8.9, 'max_time_ms': 11.5, 'std_dev_ms': 0.9},
            {'database': 'postgresql', 'method': 'xml_datatype', 'operation': 'write', 'avg_time_ms': 28.9, 'min_time_ms': 26.2, 'max_time_ms': 32.1, 'std_dev_ms': 2.0},
            {'database': 'postgresql', 'method': 'xml_datatype', 'operation': 'update', 'avg_time_ms': 20.3, 'min_time_ms': 18.1, 'max_time_ms': 23.2, 'std_dev_ms': 1.6},
            {'database': 'postgresql', 'method': 'xml_datatype', 'operation': 'search', 'avg_time_ms': 25.7, 'min_time_ms': 23.1, 'max_time_ms': 29.4, 'std_dev_ms': 2.1},
            {'database': 'postgresql', 'method': 'hybrid', 'operation': 'read', 'avg_time_ms': 9.5, 'min_time_ms': 8.2, 'max_time_ms': 11.1, 'std_dev_ms': 0.8},
            {'database': 'postgresql', 'method': 'hybrid', 'operation': 'write', 'avg_time_ms': 40.2, 'min_time_ms': 37.1, 'max_time_ms': 44.5, 'std_dev_ms': 2.8},
            {'database': 'postgresql', 'method': 'hybrid', 'operation': 'update', 'avg_time_ms': 24.6, 'min_time_ms': 22.1, 'max_time_ms': 27.8, 'std_dev_ms': 1.9},
            {'database': 'postgresql', 'method': 'hybrid', 'operation': 'search', 'avg_time_ms': 18.9, 'min_time_ms': 16.5, 'max_time_ms': 21.7, 'std_dev_ms': 1.5},
        ]
        return pd.DataFrame(demo_data)

    def generate_report(self):
        print("Генерация отчёта...")

        df = self.performance_tester.get_results_dataframe()

        if df.empty:
            print("Нет результатов тестов. Загрузка демонстрационных данных...")
            df = self._load_demo_data()

        visualizations = self.visualizer.generate_all_visualizations(df)

        report_path = self.report_generator.generate_report(
            self.performance_tester.test_results if self.performance_tester.test_results else df,
            visualizations
        )

        print(f"Отчёт сгенерирован: {report_path}")
        return report_path

    def import_dataset(self):
        print("Импорт набора данных...")

        filepath = input("Введите путь к файлу набора данных: ")
        try:
            data = self.data_handler.import_dataset(filepath)
            print(f"Набор данных успешно импортирован из {filepath}")
            self.current_dataset = data
            return data
        except Exception as e:
            print(f"Ошибка импорта набора данных: {e}")
            return None

    def export_dataset(self):
        print("Экспорт набора данных...")

        if hasattr(self, 'current_dataset'):
            filepath = input("Введите путь для сохранения набора данных: ")
            format_type = input("Введите формат (xml/json/csv/xlsx): ").lower()
            try:
                self.data_handler.export_dataset(self.current_dataset, filepath, format_type)
                print(f"Набор данных успешно экспортирован в {filepath}")
                return True
            except Exception as e:
                print(f"Ошибка экспорта набора данных: {e}")
                return False
        else:
            print("Набор данных не загружен. Сначала импортируйте набор данных.")
            return False
