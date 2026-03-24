"""
Утилиты для красивого вывода в консоль
"""
import sys
import time


class Colors:
    """ANSI цвета для консоли"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Цвета текста
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    # Цвета фона
    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"
    BG_RED = "\033[41m"


def clear_screen():
    """Очистка экрана"""
    print("\033[2J\033[H", end="")
    sys.stdout.flush()


def print_logo():
    """Вывод логотипа приложения"""
    logo = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ███╗   ██╗███████╗██╗    ██╗██╗   ██╗███████╗          ║
║   ████╗  ██║██╔════╝██║    ██║██║   ██║██╔════╝          ║
║   ██╔██╗ ██║█████╗  ██║ █╗ ██║██║   ██║███████╗          ║
║   ██║╚██╗██║██╔══╝  ██║███╗██║██║   ██║╚════██║          ║
║   ██║ ╚████║███████╗╚███╔███╔╝╚██████╔╝███████║          ║
║   ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚══════╝          ║
║                                                           ║
║        📊 Анализ методов хранения XML 📊                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(logo)


def print_header(text):
    """Вывод заголовка раздела"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'═' * 60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}  {text}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'═' * 60}{Colors.RESET}")


def print_success(text):
    """Вывод успешного сообщения"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text):
    """Вывод ошибки"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text):
    """Вывод предупреждения"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def print_info(text):
    """Вывод информационной сообщения"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def print_step(step, total, text):
    """Вывод шага выполнения"""
    print(f"{Colors.MAGENTA}[{step}/{total}]{Colors.RESET} {text}")


def print_progress_bar(current, total, bar_length=40):
    """Вывод прогресс-бара"""
    percent = float(current) / total
    arrow = '█' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    
    sys.stdout.write(f"\r  [{arrow}{spaces}] {int(percent * 100)}%")
    sys.stdout.flush()
    
    if current >= total:
        print()


def print_menu_item(key, text, description=""):
    """Вывод пункта меню"""
    print(f"  {Colors.YELLOW}[{key}]{Colors.RESET} {text}")
    if description:
        print(f"     {Colors.DIM}{description}{Colors.RESET}")


def print_table(headers, rows):
    """Вывод таблицы"""
    # Вычисление ширины колонок
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Вывод заголовка
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    separator = "-+-".join("-" * w for w in col_widths)
    
    print(f"\n  {header_row}")
    print(f"  {separator}")
    
    # Вывод строк
    for row in rows:
        row_str = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(f"  {row_str}")


def get_user_input(prompt, default=None, choices=None):
    """Получение ввода от пользователя с подсказками"""
    if default:
        prompt = f"{prompt} [{default}]"
    prompt = f"{Colors.GREEN}{prompt}{Colors.RESET}: "
    
    while True:
        try:
            value = input(prompt).strip()
            if not value and default:
                return default
            if choices and value not in choices:
                print_error(f"Неверный выбор. Доступные варианты: {', '.join(choices)}")
                continue
            return value
        except (EOFError, KeyboardInterrupt):
            print()
            return default


def confirm_action(prompt="Выполнить действие?"):
    """Запрос подтверждения"""
    result = get_user_input(f"{prompt} (y/n)", default="n", choices=["y", "n", "yes", "no"])
    return result.lower() in ["y", "yes"]


def simulate_loading(text, duration=1.0, steps=10):
    """Имитация загрузки"""
    print(f"{text}...", end="")
    for i in range(steps):
        time.sleep(duration / steps)
        sys.stdout.write(".")
        sys.stdout.flush()
    print(f" {Colors.GREEN}готово!{Colors.RESET}")
