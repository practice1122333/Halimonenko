import socket
import customtkinter as ctk  # Використовуємо CustomTkinter


def send_command_to_server(command):
    """Відправляє команду на сервер і отримує результат"""
    try:
        # Підключаємося до сервера
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8080))

        # Відправляємо команду на сервер
        client_socket.sendall(command.encode('utf-8'))

        # Отримуємо результат
        result = client_socket.recv(4096).decode('utf-8')
        client_socket.close()

        return result
    except Exception as e:
        return f"Помилка підключення: {e}"


def on_execute_command(command):
    """Обробляє натискання кнопки для виконання команди"""
    result = send_command_to_server(command)

    # Виводимо результат у текстове поле
    result_text.delete(1.0, ctk.END)
    result_text.insert(ctk.END, result)


# Створення вікна CustomTkinter
ctk.set_appearance_mode("dark")  # Встановлюємо темну тему
ctk.set_default_color_theme("blue")  # Можна змінити на інші кольори

root = ctk.CTk()  # Вікно
root.title("Керування системою через PowerShell")

# Створення основного контейнера
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Список кнопок для команд
buttons = [
    ("Перевірити процеси", "check_system"),
    ("Перевірити брандмауер", "check_firewall"),
    ("Перевірити використання диска", "check_disk_usage"),
    ("Перевірити мережу", "check_network"),
    ("Перевірити оновлення", "check_update"),
    ("Перевірити CPU", "check_cpu_usage"),
    ("Перевірити пам'ять", "check_memory_usage"),
    ("Перевірити сервіси", "check_service"),
    ("Перевірити безпеку", "check_security"),
    ("Перевірити журнали", "check_logs"),
    ("Зупинити процес", "react_shutdown_process"),
    ("Увімкнути брандмауер", "react_enable_firewall"),
    ("Вимкнути брандмауер", "react_disable_firewall"),
    ("Очищення диска", "react_clear_disk"),
    ("Перезапуск мережі", "react_restart_network"),
    ("Оновлення системи", "react_update_system"),
    ("Перезавантаження сервісу", "react_restart_service"),
    ("Виправлення безпеки", "react_security_fix"),
    ("Очищення журналів", "react_clear_logs")
]

# Використовуємо grid для рівного розташування кнопок
row = 0
col = 0
button_width = 40  # Ширина кнопок

for label, command in buttons:
    button = ctk.CTkButton(frame, text=label, width=300, height=40, command=lambda cmd=command: on_execute_command(cmd))
    button.grid(row=row, column=col, padx=10, pady=10, sticky="w")

    # Встановлюємо розташування кнопок в сітці
    col += 1
    if col > 2:  # Якщо більше 3 кнопок в рядку, переходимо на новий рядок
        col = 0
        row += 1

# Текстове поле для виведення результатів
result_text = ctk.CTkTextbox(root, width=80, height=15, wrap="word")
result_text.pack(pady=20, padx=20, fill="both", expand=True)

# Запуск інтерфейсу
root.mainloop()
