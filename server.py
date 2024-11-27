import socket
import subprocess

# Словник команд і відповідних рекомендацій
commands_with_recommendations = {
    "check_system": ("Get-Process", "Перевірте процеси, які займають занадто багато ресурсів."),
    "check_firewall": ("Get-NetFirewallProfile", "Перевірте налаштування брандмауера на наявність уразливих правил."),
    "check_disk_usage": ("Get-PSDrive -PSProvider FileSystem", "Перевірте вільний простір на диску для уникнення збоїв."),
    "check_network": ("Test-NetConnection -ComputerName google.com", "Перевірте налаштування мережі та з'єднання."),
    "check_update": ("Get-WindowsUpdateLog", "Перевірте журнали оновлень на наявність помилок."),
    "check_cpu_usage": ("Get-WmiObject Win32_Processor", "Перевірте використання процесора на наявність високих значень."),
    "check_memory_usage": ("Get-WmiObject Win32_OperatingSystem", "Перевірте використання пам'яті для запобігання перевантаженню."),
    "check_service": ("Get-Service", "Перевірте статус важливих системних сервісів."),
    "check_security": ("Get-WindowsUpdateLog | Select-String 'Security'", "Перевірте наявність критичних оновлень безпеки."),
    "check_logs": ("Get-EventLog -LogName System -EntryType Error", "Перевірте системні журнали на наявність помилок."),
    "react_shutdown_process": ("Stop-Process -Name 'exampleprocess'", "Зупиніть процес, якщо він споживає занадто багато ресурсів."),
    "react_enable_firewall": ("Set-NetFirewallProfile -Enabled True", "Увімкніть брандмауер для посилення безпеки."),
    "react_disable_firewall": ("Set-NetFirewallProfile -Enabled False", "Вимкніть брандмауер тимчасово для усунення конфліктів."),
    "react_clear_disk": ("Clear-Disk -RemoveData", "Очищення диска для звільнення місця."),
    "react_restart_network": ("Restart-Service -Name 'netsh'", "Перезапуск мережевих служб для відновлення з'єднання."),
    "react_update_system": ("Start-Process -FilePath 'C:\\Windows\\System32\\wuauclt.exe' -ArgumentList '/detectnow'", "Перевірте наявність оновлень для покращення безпеки."),
    "react_restart_service": ("Restart-Service -Name 'example_service'", "Перезапустіть сервіс, якщо він не працює належним чином."),
    "react_security_fix": ("Install-WindowsUpdate -AcceptAll -IgnoreReboot", "Встановіть останні оновлення безпеки."),
    "react_clear_logs": ("Clear-EventLog -LogName System", "Очистіть системні журнали для покращення продуктивності.")
}

def execute_powershell_command(command):
    """Виконує команду PowerShell і повертає результат"""
    try:
        result = subprocess.check_output(["powershell", "-Command", command], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Помилка при виконанні команди: {e.output}"

def handle_command(command):
    """Обробка команд та надання рекомендацій"""
    if command in commands_with_recommendations:
        ps_command, recommendation = commands_with_recommendations[command]
        command_output = execute_powershell_command(ps_command)
        return command_output, recommendation
    else:
        return "Невідома команда", "Немає рекомендацій."

def start_server():
    """Запуск сервера для отримання команд від клієнта"""
    host = 'localhost'
    port = 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Сервер запущено на {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Підключено до {addr}")

        # Отримуємо команду від клієнта
        command = client_socket.recv(1024).decode('utf-8')
        print(f"Отримано команду: {command}")

        # Обробка команди та отримання результату і рекомендацій
        output, recommendation = handle_command(command)

        # Відправляємо результат та рекомендації клієнту
        client_socket.sendall(f"Результат виконання: \n{output}\nРекомендація: {recommendation}".encode('utf-8'))

        # Закриваємо з'єднання
        client_socket.close()

if __name__ == "__main__":
    start_server()
