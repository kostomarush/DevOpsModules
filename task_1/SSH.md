1. Создать SSH-ключи и проверить их работоспособность: 
   `ssh-keygen -t rsa -b 4096` через scp передал публичный ключ на ВМ ubuntu, и добавил его в authorized_keys `cat id_rsa.pub >> authorized_keys`. После чего подключился к ВМ по ssh по ключу
2. Отключил аутентификацию по паролю в `/etc/ssh/sshd_config` параметр `PasswordAuthentication no`
3. Включив `PubkeyAuthentication yes`
4. Перезагрузил демон systemctl и  ssh сервер. Проверил работоспособность