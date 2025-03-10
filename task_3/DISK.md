1. Установил ОС ubuntu на ВМ на среде виртуализации vmware
2. Подключил дополнительный жесткий диск на 2 гб (перезагрузил ОС)
3. Проверил подключенный диск с помощью `lsblk`
4. Установил утилиту GFS2 `sudo apt install -y corosync pacemaker gfs2-utils dlm-controld` а таже необходимые утилиты для корректной работы в кластере:
	- `corosync` (указал в конфиге название созданного кластера)
	- `pacemaker`
	- `dlm`
5. Создал GFS2 на данном диске `sudo mkfs.gfs2 -p lock_dlm -t cluster_ubuntu:clusterfs -j 2 /dev/sdb`
6. Проверил ФС `sudo blkid /dev/sdb`
7. Примонтировал данный диск в /mnt/cluster_disk
8. Добавил запись в /etc/fstab: `UUID=13804663-b8af-4a3f-8f79-5ca0265c7a13 /mnt/cluster_disk/ gfs2 defaults,_netdev,x-systemd.requires=dlm.service 0 0`
	- `_netdev` — указывает, что диск требует сетевых сервисов (чтобы загружался после Corosync/DLM).
	- `x-systemd.requires=dlm.service` — гарантирует, что диск будет монтироваться **только после старта DLM**.
9. Проверил командой `mount -a`



