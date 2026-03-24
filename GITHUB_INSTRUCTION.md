# Инструкция по загрузке на GitHub

## 1. Создайте репозиторий на GitHub

1. Перейдите на https://github.com
2. Войдите в свой аккаунт
3. Нажмите **+** в правом верхнем углу → **New repository**
4. Введите имя репозитория (например, `xml-storage-analysis`)
5. Выберите тип доступа: **Public** или **Private**
6. **НЕ ставьте** галочки на "Initialize with README", ".gitignore", "license"
7. Нажмите **Create repository**

## 2. Загрузите проект на GitHub

Откройте PowerShell в папке проекта и выполните команды:

```powershell
cd "c:\РАБОТА\маша курсач"

# Подключите удалённый репозиторий (замените YOUR_USERNAME и REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/xml-storage-analysis.git

# Загрузите файлы
git push -u origin main
```

## 3. Проверка загрузки

1. Обновите страницу репозитория на GitHub
2. Вы должны увидеть все файлы проекта

---

# Инструкция по запуску проекта

## Быстрый старт

```bash
# Запуск в интерактивном режиме (меню)
python main.py

# Запуск с конфигурацией
python main.py --config config.json --action visualize
python main.py --config config.json --action report
```

## Доступные команды

| Команда | Описание |
|---------|----------|
| `python main.py` | Интерактивный режим с меню |
| `python main.py --config config.json --action test` | Запуск тестов производительности (нужны БД) |
| `python main.py --config config.json --action visualize` | Генерация визуализаций |
| `python main.py --config config.json --action report` | Генерация HTML-отчёта |
| `python main.py --config config.json --action import` | Импорт набора данных |
| `python main.py --config config.json --action export` | Экспорт набора данных |

## Примечания

- Предупреждения `mkdir -p failed` от matplotlib **не критичны** — приложение работает нормально
- Для полноценного тестирования производительности нужны запущенные СУБД (PostgreSQL, MySQL или SQL Server)
- Без БД доступны демонстрационные визуализации и отчёты

## Структура проекта

```
c:\РАБОТА\маша курсач\
├── main.py                 # Точка входа
├── app/                    # Модули приложения
│   ├── application.py
│   ├── database_manager.py
│   ├── storage_methods.py
│   ├── performance_tester.py
│   ├── visualizer.py
│   ├── report_generator.py
│   ├── data_handler.py
│   └── config_manager.py
├── config.json             # Конфигурация
├── requirements.txt        # Зависимости
├── docs/                   # Документация
├── results/                # Результаты тестов
├── reports/                # Отчёты
└── visualizations/         # Визуализации
```
