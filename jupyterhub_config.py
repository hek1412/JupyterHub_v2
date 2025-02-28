from dockerspawner import DockerSpawner
import os, nativeauthenticator
c = get_config()

# Основные настройки JupyterHub
c.JupyterHub.bind_url = 'http://:8000'
c.JupyterHub.hub_bind_url = 'http://0.0.0.0:8081'
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator" # Назначаем класс аутентификации
c.NativeAuthenticator.check_common_password = True # Включает проверку на наличие распространенных паролей
c.NativeAuthenticator.allowed_users = {'admin'} # Устанавливает, что только указанный пользователь может использовать систему
c.NativeAuthenticator.admin_users = {'admin'} # Задает администратора JupyterHub.
c.NativeAuthenticator.allowed_failed_logins = 3 # Определяет число неудачных попыток входа, после которых пользователь будет временно заблокирован
c.NativeAuthenticator.seconds_before_next_try = 1200 # Устанавливает время блокировки в секундах после превышения попыток входа (20 минут).
c.Authenticator.open_signup = True # позволяют пользователям регистрироваться самостоятельно 
c.Authenticator.allow_all = True # всем зарегистрированным пользователям позволяет входить в систему
c.JupyterHub.shutdown_on_logout = True # автоматически останавливает сервер пользователя, как только он выходит из системы
c.DockerSpawner.remove_containers = True

# Настраиваем Spawner для использования Docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = 'hek1412/my-jupyter-test:v1' # Указывает образ Docker, который будет использоваться для запуска каждого пользователя
c.Spawner.http_timeout = 180 # указывает максимальное время (в секундах), в течение которого JupyterHub будет ожидать, что спаунер (Spawner) запустит сервер пользователя
c.DockerSpawner.network_name = "jupyterhub-network" # Имя сети Docker, которое будет использоваться
c.Spawner.start_timeout = 240 # временной интервал в секундах, после которого процесс запуска будет считаться неудачным, если не завершится

# Настройка монтирования тома для каждого пользователя
notebook_dir = '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir # Каталог, который будет монтироваться в контейнере для хранения файлов Jupyter
# Задаем монтирование: общий том с поддиректориями для каждого пользователя
c.DockerSpawner.volumes = { 'jupyterhub-data_v2_{username}': '/home/jovyan/work'}

# доп настройки
c.DockerSpawner.remove = True # Автоматически удаляет контейнеры после их остановки (может быть убрать, что бы не слетала среда)
c.DockerSpawner.debug = True # Включает отладку для более детальной диагностики, если что-то пойдет не так
# c.DockerSpawner.cpu_limit = 4 # лимиты CPU
# c.DockerSpawner.mem_limit = '16G' # лимиты памяти
c.JupyterHub.active_server_limit = 6 # максимальное количество активных серверов
c.JupyterHub.shutdown_no_activity_timeout = 600 #  Таймаут для автоматического завершения работы контейнеров при отсутствии активности (10 минут)
c.JupyterHub.shutdown_on_logout = True # автоматически останавливает сервер пользователя, как только он выходит из системы

# Настроить команду запуска для jupyterhub-singleuser
c.DockerSpawner.extra_create_kwargs = {
    'runtime': 'nvidia'
}
# Настроить дополнительные параметры для GPU
c.DockerSpawner.extra_host_config = {
    'device_requests': [
        {
            'Driver': 'nvidia',
            'Count': -1,
            'Capabilities': [['gpu']],
        }
    ]
}

data_dir = '/srv/jupyterhub/data' # дирректория для секретов
c.JupyterHub.cookie_secret_file = os.path.join(data_dir, 'jupyterhub_cookie_secret') # параметр указывает путь к файлу, который хранит секретные данные для куки-файлов, используемые для обеспечения безопасности сеансов пользователей в JupyterHub
c.JupyterHub.db_url = "sqlite:////srv/jupyterhub/data/jupyterhub.sqlite" # Указывает использовать SQLite для хранения данных JupyterHub
c.JupyterHub.log_level = 'DEBUG' # Устанавливает уровень логирования на DEBUG
# Сбор метрик
c.JupyterHub.metrics_enabled = True
c.JupyterHub.metrics_port = 8000
c.JupyterHub.authenticate_prometheus = False



