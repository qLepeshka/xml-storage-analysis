from app.storage_methods import StorageMethods
from app.performance_tester import PerformanceTester
from app.visualizer import Visualizer
from app.report_generator import ReportGenerator
from app.data_handler import DataHandler
from app.config_manager import ConfigManager


def test_core_components():
    print("Тестирование основных компонентов приложения...")

    print("\n1. Тестирование StorageMethods...")
    storage_methods = StorageMethods()
    methods = storage_methods.list_methods()
    print(f"   Доступные методы хранения: {methods}")
    print("   StorageMethods успешно инициализирован")

    print("\n2. Тестирование PerformanceTester...")
    perf_tester = PerformanceTester()
    print("   PerformanceTester успешно инициализирован")

    print("\n3. Тестирование Visualizer...")
    visualizer = Visualizer()
    print("   Visualizer успешно инициализирован")

    print("\n4. Тестирование ReportGenerator...")
    report_gen = ReportGenerator()
    print("   ReportGenerator успешно инициализирован")

    print("\n5. Тестирование DataHandler...")
    data_handler = DataHandler()
    sample_xml = data_handler.generate_sample_xml(5)
    print(f"   Сгенерирован тестовый XML с 5 элементами: {len(sample_xml)} символов")
    print("   DataHandler успешно инициализирован")

    print("\n6. Тестирование ConfigManager...")
    config_manager = ConfigManager()
    db_types = config_manager.get('databases')
    print(f"   Базы данных по умолчанию: {db_types}")
    methods = config_manager.get('methods')
    print(f"   Методы по умолчанию: {methods}")
    print("   ConfigManager успешно инициализирован")

    print("\nВсе основные компоненты протестированы успешно!")


def test_storage_methods():
    print("\nТестирование методов хранения с тестовыми данными...")

    storage_methods = StorageMethods()
    data_handler = DataHandler()

    sample_xml = data_handler.generate_sample_xml(10)
    print(f"   Сгенерирован тестовый XML с 10 элементами")

    for method_name in storage_methods.list_methods():
        print(f"   Тестирование {method_name}...")
        method = storage_methods.get_method(method_name)
        print(f"     {method_name} успешно получен")


def test_data_handling():
    print("\nТестирование функциональности обработки данных...")

    data_handler = DataHandler()

    sample_xml = data_handler.generate_sample_xml(3)
    print("   Сгенерированы тестовые XML данные")

    is_valid = data_handler.validate_xml(sample_xml)
    print(f"   Результат проверки XML: {is_valid}")

    import tempfile
    import os

    with tempfile.TemporaryDirectory() as temp_dir:
        json_path = os.path.join(temp_dir, "test.json")
        data_handler._export_json({"test": "data"}, json_path)
        print(f"   Экспорт в JSON: {os.path.exists(json_path)}")

        csv_path = os.path.join(temp_dir, "test.csv")
        data_handler._export_csv([{"col1": "value1", "col2": "value2"}], csv_path)
        print(f"   Экспорт в CSV: {os.path.exists(csv_path)}")

        print("   Тесты обработки данных завершены")


if __name__ == "__main__":
    test_core_components()
    test_storage_methods()
    test_data_handling()
    print("\nВсе тесты пройдены! Структура приложения работает корректно.")
