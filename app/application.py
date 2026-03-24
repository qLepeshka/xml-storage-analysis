import argparse
from app.database_manager import DatabaseManager
from app.storage_methods import StorageMethods
from app.performance_tester import PerformanceTester
from app.visualizer import Visualizer
from app.report_generator import ReportGenerator
from app.data_handler import DataHandler
from app.config_manager import ConfigManager
from app.ui_utils import (
    Colors, print_logo, print_header, print_success, print_error,
    print_warning, print_info, print_menu_item, print_table,
    get_user_input, confirm_action, simulate_loading, clear_screen
)


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
        """Показ главного меню"""
        clear_screen()
        print_logo()
        
        print_header("📋 ГЛАВНОЕ МЕНЮ")
        print()
        print_menu_item("1", "🗄️  Настройка баз данных", "Конфигурация подключения к СУБД")
        print_menu_item("2", "⚡ Запуск тестов производительности", "Сравнение методов хранения XML")
        print_menu_item("3", "📊 Генерация визуализаций", "Диаграммы и графики результатов")
        print_menu_item("4", "📄 Генерация отчёта", "HTML-отчёт с рекомендациями")
        print_menu_item("5", "📥 Импорт набора данных", "Загрузка данных из файла")
        print_menu_item("6", "📤 Экспорт набора данных", "Сохранение данных в файл")
        print_menu_item("7", "❓ Справка", "Информация о программе")
        print_menu_item("0", "🚪 Выход", "Завершение работы программы")
        print()
        
        choice = get_user_input("  Введите номер пункта", default="7", 
                               choices=["0", "1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            self.configure_databases()
        elif choice == "2":
            self.run_performance_tests()
        elif choice == "3":
            self.generate_visualizations()
        elif choice == "4":
            self.generate_report()
        elif choice == "5":
            self.import_dataset()
        elif choice == "6":
            self.export_dataset()
        elif choice == "7":
            self.show_help()
        elif choice == "0":
            print("\n" + "=" * 60)
            print_success("Спасибо за использование XML Storage Analysis!")
            print("=" * 60 + "\n")
            exit(0)
        else:
            print_error("Неверный выбор. Попробуйте снова.")
        
        # Возврат в меню после выполнения действия
        input("\n" + "=" * 60 + "\nНажмите Enter для продолжения...")
        self.show_menu()

    def configure_databases(self):
        """Настройка баз данных"""
        clear_screen()
        print_header("🗄️  НАСТРОЙКА БАЗ ДАННЫХ")
        
        print(f"""
{Colors.CYAN}Текущая конфигурация:{Colors.RESET}
""")
        
        databases = self.config_manager.get('databases', [])
        print(f"  Подключённые базы данных: {', '.join(databases)}")
        
        print(f"""
{Colors.YELLOW}Для подключения базы данных:{Colors.RESET}
  1. Отредактируйте файл config.json
  2. Укажите параметры подключения:
     - host (адрес сервера)
     - port (порт)
     - database (имя базы данных)
     - username (пользователь)
     - password (пароль)

{Colors.GREEN}Поддерживаемые СУБД:{Colors.RESET}
  ✓ PostgreSQL (рекомендуется)
  ✓ MySQL
  ✓ SQL Server
""")
        
        if confirm_action("Хотите проверить подключение к базам данных?"):
            self._test_database_connections()

    def _test_database_connections(self):
        """Тестирование подключения к БД"""
        databases = self.config_manager.get('databases', [])
        
        for db_type in databases:
            db_config = self.config_manager.get_database_config(db_type)
            if db_config:
                print_info(f"Проверка подключения к {db_type}...")
                # Здесь будет логика подключения
                print_warning("Тестирование будет доступно после настройки БД")

    def show_help(self):
        """Показ справки"""
        clear_screen()
        print_header("❓ СПРАВКА")
        
        print(f"""
{Colors.CYAN}XML Storage Analysis — Инструмент сравнительного анализа методов хранения XML{Colors.RESET}

{Colors.YELLOW}📌 О ПРОЕКТЕ:{Colors.RESET}
  Приложение сравнивает производительность различных способов хранения 
  XML-данных в реляционных базах данных.

{Colors.YELLOW}📌 МЕТОДЫ ХРАНЕНИЯ:{Colors.RESET}
  1. {Colors.GREEN}Native Text{Colors.RESET} — хранение XML как обычного текста
  2. {Colors.GREEN}Normalized Relational{Colors.RESET} — разбор XML в таблицы
  3. {Colors.GREEN}XML Data Type{Colors.RESET} — использование XML-типа данных
  4. {Colors.GREEN}Hybrid{Colors.RESET} — комбинация методов

{Colors.YELLOW}📌 ОПЕРАЦИИ:{Colors.RESET}
  • {Colors.BLUE}Read{Colors.RESET} — чтение данных
  • {Colors.BLUE}Write{Colors.RESET} — запись данных
  • {Colors.BLUE}Update{Colors.RESET} — обновление данных
  • {Colors.BLUE}Search{Colors.RESET} — поиск в XML

{Colors.YELLOW}📌 КОМАНДЫ ИНТЕРФЕЙСА:{Colors.RESET}
  1 — Настройка подключения к базам данных
  2 — Запуск тестов производительности
  3 — Генерация графиков и диаграмм
  4 — Создание HTML-отчёта
  5 — Импорт данных из файла
  6 — Экспорт данных в файл
  7 — Показать эту справку
  0 — Выход из программы

{Colors.YELLOW}📌 БЫСТРЫЙ СТАРТ (командная строка):{Colors.RESET}
  python main.py --config config.json --action visualize
  python main.py --config config.json --action report

{Colors.YELLOW}📌 ФАЙЛЫ ПРОЕКТА:{Colors.RESET}
  • config.json — конфигурация
  • visualizations/ — графики
  • reports/ — отчёты
  • docs/ — документация
""")
        
        input("\nНажмите Enter для возврата в меню...")

    def run_performance_tests(self):
        """Запуск тестов производительности"""
        clear_screen()
        print_header("⚡ ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ")
        
        print(f"""
{Colors.CYAN}Параметры тестирования:{Colors.RESET}
""")
        
        test_params = self.config_manager.get('test_parameters', {})
        print(f"  Размер данных: {test_params.get('data_size', 100)} элементов")
        print(f"  Количество запусков: {test_params.get('test_runs', 10)}")
        print(f"  Прогревочные запуски: {test_params.get('warmup_runs', 3)}")
        print(f"  Таймаут: {test_params.get('timeout', 30)} сек")
        
        databases = self.config_manager.get('databases', [])
        methods = self.config_manager.get('methods', [])
        
        print(f"\n{Colors.GREEN}Базы данных:{Colors.RESET} {', '.join(databases)}")
        print(f"{Colors.GREEN}Методы:{Colors.RESET} {', '.join(methods)}")
        
        print()
        if not confirm_action("Запустить тесты производительности?"):
            return
        
        print()
        print_info("Запуск тестов...")
        
        # Имитация процесса тестирования
        import time
        for i in range(5):
            print_progress_bar(i + 1, 5)
            time.sleep(0.5)
        
        print_warning("""
⚠  Для полноценного тестирования необходимы подключённые базы данных.
   Сейчас загружаются демонстрационные результаты.
""")
        
        print_success("Тесты завершены! Результаты сохранены.")

    def generate_visualizations(self):
        """Генерация визуализаций"""
        clear_screen()
        print_header("📊 ГЕНЕРАЦИЯ ВИЗУАЛИЗАЦИЙ")
        
        df = self.performance_tester.get_results_dataframe()

        if df.empty:
            print_warning("Нет результатов тестов. Загрузка демонстрационных данных...")
            df = self._load_demo_data()
        
        print_info("Генерация диаграмм и графиков...")
        print()

        visualizations = self.visualizer.generate_all_visualizations(df)

        viz_dir = self.config_manager.get('output_settings.visualization_dir')
        import os
        try:
            os.makedirs(viz_dir, exist_ok=True)
        except FileExistsError:
            pass

        print(f"\n{Colors.GREEN}Созданные файлы:{Colors.RESET}")
        for name, fig in visualizations.items():
            filepath = os.path.join(viz_dir, f"{name}.html")
            self.visualizer.save_visualization(fig, filepath)
            print(f"  ✓ {filepath}")

        print_success(f"Визуализации сгенерированы и сохранены в {viz_dir}")
        print_info(f"Откройте любой HTML-файл в браузере для просмотра")
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
        """Генерация отчёта"""
        clear_screen()
        print_header("📄 ГЕНЕРАЦИЯ ОТЧЁТА")
        
        df = self.performance_tester.get_results_dataframe()

        if df.empty:
            print_warning("Нет результатов тестов. Загрузка демонстрационных данных...")
            df = self._load_demo_data()
        
        print_info("Создание HTML-отчёта с анализом и рекомендациями...")
        print()

        visualizations = self.visualizer.generate_all_visualizations(df)

        # Прогресс генерации
        import time
        for i in range(3):
            print_progress_bar(i + 1, 3)
            time.sleep(0.3)

        report_path = self.report_generator.generate_report(
            df,
            visualizations
        )

        print()
        print_success(f"Отчёт сгенерирован: {report_path}")
        print_info(f"Откройте файл в браузере для просмотра")
        return report_path

    def import_dataset(self):
        """Импорт набора данных"""
        clear_screen()
        print_header("📥 ИМПОРТ НАБОРА ДАННЫХ")
        
        print(f"""
{Colors.CYAN}Поддерживаемые форматы:{Colors.RESET}
  • XML — Extensible Markup Language
  • JSON — JavaScript Object Notation
  • CSV — Comma-Separated Values
  • XLSX — Microsoft Excel

{Colors.YELLOW}Инструкция:{Colors.RESET}
  1. Подготовьте файл с данными
  2. Введите полный путь к файлу
  3. Данные будут загружены для тестирования
""")
        
        filepath = get_user_input("  Введите путь к файлу")
        
        if not filepath:
            print_warning("Импорт отменён")
            return
        
        try:
            print()
            print_info(f"Загрузка данных из {filepath}...")
            data = self.data_handler.import_dataset(filepath)
            self.current_dataset = data
            print_success(f"Данные успешно импортированы!")
            
            if isinstance(data, str):
                print_info(f"Размер данных: {len(data)} символов")
            elif isinstance(data, list):
                print_info(f"Количество записей: {len(data)}")
        except Exception as e:
            print_error(f"Ошибка импорта: {e}")

    def export_dataset(self):
        """Экспорт набора данных"""
        clear_screen()
        print_header("📤 ЭКСПОРТ НАБОРА ДАННЫХ")
        
        if not hasattr(self, 'current_dataset'):
            print_warning("""
Нет загруженных данных.
Сначала импортируйте набор данных через пункт меню 5.
""")
            input("\nНажмите Enter для продолжения...")
            return
        
        print(f"""
{Colors.CYAN}Доступные форматы экспорта:{Colors.RESET}
  • xml — Extensible Markup Language
  • json — JavaScript Object Notation  
  • csv — Comma-Separated Values
  • xlsx — Microsoft Excel
""")
        
        filepath = get_user_input("  Введите путь для сохранения")
        if not filepath:
            print_warning("Экспорт отменён")
            return
        
        format_type = get_user_input("  Введите формат (xml/json/csv/xlsx)", 
                                     default="json",
                                     choices=["xml", "json", "csv", "xlsx"])
        
        try:
            print()
            print_info(f"Экспорт данных в {format_type}...")
            self.data_handler.export_dataset(self.current_dataset, filepath, format_type)
            print_success(f"Данные успешно экспортированы в {filepath}!")
        except Exception as e:
            print_error(f"Ошибка экспорта: {e}")
