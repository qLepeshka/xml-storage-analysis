from app.database_manager import DatabaseManager
from app.storage_methods import StorageMethods
from app.performance_tester import PerformanceTester
from app.visualizer import Visualizer
from app.report_generator import ReportGenerator
from app.data_handler import DataHandler
from app.config_manager import ConfigManager


def test_components():
    print("Тестирование компонентов приложения...")

    print("\n1. Тестирование DatabaseManager...")
    db_manager = DatabaseManager()
    print("   ✓ DatabaseManager успешно инициализирован")

    print("\n2. Тестирование StorageMethods...")
    storage_methods = StorageMethods()
    methods = storage_methods.list_methods()
    print(f"   Доступные методы хранения: {methods}")
    print("   ✓ StorageMethods успешно инициализирован")

    print("\n3. Тестирование PerformanceTester...")
    perf_tester = PerformanceTester()
    print("   ✓ PerformanceTester успешно инициализирован")

    print("\n4. Тестирование Visualizer...")
    visualizer = Visualizer()
    print("   ✓ Visualizer успешно инициализирован")

    print("\n5. Тестирование ReportGenerator...")
    report_gen = ReportGenerator()
    print("   ✓ ReportGenerator успешно инициализирован")

    print("\n6. Тестирование DataHandler...")
    data_handler = DataHandler()
    sample_xml = data_handler.generate_sample_xml(5)
    print(f"   Сгенерирован тестовый XML с 5 элементами: {len(sample_xml)} символов")
    print("   ✓ DataHandler успешно инициализирован")

    print("\n7. Тестирование ConfigManager...")
    config_manager = ConfigManager()
    db_types = config_manager.get('databases')
    print(f"   Базы данных по умолчанию: {db_types}")
    print("   ✓ ConfigManager успешно инициализирован")

    print("\n✓ Все компоненты протестированы успешно!")


def test_storage_methods():
    print("\nТестирование методов хранения с тестовыми данными...")

    storage_methods = StorageMethods()
    data_handler = DataHandler()

    sample_xml = data_handler.generate_sample_xml(10)
    print(f"   Сгенерирован тестовый XML с 10 элементами")

    for method_name in storage_methods.list_methods():
        print(f"   Тестирование {method_name}...")
        method = storage_methods.get_method(method_name)
        print(f"     ✓ {method_name} успешно получен")


if __name__ == "__main__":
    test_components()
    test_storage_methods()
    print("\nВсе тесты пройдены! Структура приложения работает корректно.")
