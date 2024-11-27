import socket
import customtkinter as ctk
import os
import platform
import subprocess
import time


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


def generate_report():
    """Функція для генерації повноцінного звіту"""
    # Отримуємо час для імені файлу
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    report_file = os.path.join(desktop_path, f"system_report_{current_time}.txt")

    with open(report_file, 'w') as file:
        # Створюємо звіт
        file.write("Звіт по системі:\n\n")
        file.write("1. Перевірка процесів:\n")
        processes_result = send_command_to_server("check_system")
        file.write(processes_result + "\n\n")

        file.write("2. Перевірка брандмауера:\n")
        firewall_result = send_command_to_server("check_firewall")
        file.write(firewall_result + "\n\n")

        file.write("3. Перевірка мережі:\n")
        network_result = send_command_to_server("check_network")
        file.write(network_result + "\n\n")

        file.write("4. Перевірка диска:\n")
        disk_result = send_command_to_server("check_disk_usage")
        file.write(disk_result + "\n\n")

        file.write("5. Перевірка оновлень:\n")
        update_result = send_command_to_server("check_update")
        file.write(update_result + "\n\n")

        # Додаємо рекомендації
        file.write("Рекомендації:\n")

        if "error" in processes_result.lower():
            file.write("- Перевірте наявність завислих процесів.\n")
        if "error" in firewall_result.lower():
            file.write("- Перевірте налаштування брандмауера.\n")
        if "low disk" in disk_result.lower():
            file.write("- Звільніть місце на диску.\n")
        if "update available" in update_result.lower():
            file.write("- Виконайте оновлення системи.\n")

    # Повідомляємо користувача про успішне створення звіту
    result_text.delete(1.0, ctk.END)
    result_text.insert(ctk.END, f"Звіт згенеровано: {report_file}")


def check_permissions():
    """Перевірка прав доступу та вирішення проблем"""
    try:
        # Для Windows можна використовувати команду net user для перевірки прав
        result = subprocess.check_output("net user", shell=True).decode('utf-8')
        if "Administrator" in result:
            return "Права доступу: Відповідають вимогам"
        else:
            return "Права доступу: Не вистачає прав адміністратора"
    except Exception as e:
        return f"Помилка при перевірці прав доступу: {e}"


def on_check_permissions():
    """Обробляє натискання кнопки для перевірки прав доступу"""
    permissions_result = check_permissions()
    result_text.delete(1.0, ctk.END)
    result_text.insert(ctk.END, permissions_result)


# Створення вікна CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Аналіз системи та генерація звіту")

# Основний контейнер
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Кнопки
button_analyze = ctk.CTkButton(frame, text="Провести аналіз та згенерувати звіт", width=300, height=40,
                               command=generate_report)
button_analyze.grid(row=0, column=0, padx=10, pady=10, sticky="w")

button_permissions = ctk.CTkButton(frame, text="Перевірити права доступу", width=300, height=40,
                                   command=on_check_permissions)
button_permissions.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Текстове поле для виведення результатів
result_text = ctk.CTkTextbox(root, width=80, height=15, wrap="word")
result_text.pack(pady=20, padx=20, fill="both", expand=True)

# Запуск інтерфейсу
root.mainloop()
