# mgr5back
mgr5back - программка для бэкапирования виртуальных машин программного продукта ISP VMmanager 5 

Развертывание 
<br>git clone https://github.com/ruslansvs2/mgr5back.git
<br>Описание содержимого в каталоге 
<br>2.1 cd mgr5backup; ls -al 
<br>2.2 файлы
      config.ini  - конфигурационный файл 
      mgr5backup.py - скрипт бекапа 
      README.md - файл readme 
<br>Установка модулей 
<br>3.1 Актуальная установка модулей описана в файле README.md 
<br>Конфигурация config.ini 
<br>4.1 cat config.ini

##############################################
<br><b3>Main config for mgr5backup.py<b3>
<br>[main]
<br>\#ID vmmanager of your node
<br>NodeID: 2
<br>\#exclude the virtual machines which should not be backup.
<br>\# example NoBackupID='51,12' - ids are separeted by commas.
<br>NoBackupID: 167,173
<br>\# Connect to ftp server via the vmmgr-backup storage.
<br>ftp_conn: /usr/local/mgr5/etc/.vmmgr-backup/storages/st_3
<br>\# Pidfile
<br>pidfile: /tmp/mgr5back.pid
<br>\# Backup directory
BackDir: /backup
# Connect to database via the vmmgr config file
#FileDB: /usr/local/mgr5/etc/vmmgr.conf.d/db.conf
FileDB: /usr/local/mgr5/etc/vmmgr.conf.d/db.conf
# You can use script with gzip and without zipping, YES or NO
Gzip: YES
# How many days keep the backup files
SaveDate: 30
# Approximate period of time the backing up process, min 1 day
checkdate: 8
# The mark file of zabbix
ZabbixMarkFile: /tmp/ZabbixMark.log 
# The LVM mark file of zabbix 
ZabbixLVMFile: /tmp/ZabbixLVM.log
# The FTP mark file of zabbix 
ZabbixFTPFile: /tmp/ZabbixFTP.log

#######################################################
Help функция
start - Start full backup
id - Start backup only one VM, using by id number, example: ./mgr5backup.py id 15
list - Display the virtual machine list
status - Status of process
chftp - Check data into your ftp server
chlvm - Start check the logical volumes
chfull - Full check
ftpold - Show old or excess directories in the Node ID directory of the ftp server
ftpdel - Remove some file or directory on the FTP server
clean - Remove old or excess directories in the Node ID directory of the ftp server
zabbix-marks - Create all zabbix marks
help - Print help

Запуск бекапа 
6.1 ./mgr5back.py start   – запустит полный бекап всех виртуальных машин кроме  NoBackupID 
6.2 ./mgr5back.py id  151  – запуск бекапа виртуальной машины с id 151
 Вывод всех виртуальных машин 
7.1 ./mgr5back.py list 
Статус 
8.1 ./mgr5back.py status  – вывод статуса программки
Проверка бекапов 
9.1 Проверка LVM
9.1.1  ./mgr5back.py chlvm   – проверит ошибки на уровни LVM 
вывод  LVM OK  – все без ошибок 
или      LVM Error  - ошибка, выполните lvs, возможно после бекапа не удалось удалить логический раздел   

9.2 Проверка наличия бекапа на FTP сервере 
9.2.1  ./mgr5back.py chftp  
вывод 
Start checking the ftp server
Check the volume vm13798, the virtual machine ID 134
Check DIR 134 is Ok
Check a file vm13798_20170404020002 is OK  
Check the volume vm14913, the virtual machine ID 176
The virtual machine ID 176, have not the directory name like 176, it's ERROR
Check period of date 20170404000000
FTP Server ERROR 

тут происходит проверка на наличия папок и файлов на стороне ftp сервера.
  ./mgr5back.py chfull  – объединяет проверку chlvm и chftp 
Удаление лишних файлов и папок на бекап сервере. 
11.1  ./mgr5back.py clean 
11.1.a Вывод при удаление, на бекап сервере лишней или старой директории бекапа VM c ID 600 
Start remove old or excess directories in the Node ID directory of the ftp server
Remove a directory 600
FTP server has been cleaned,bye! 
11.1.b  вывод без удаления, файлы  консинстентны
Start remove old or excess directories in the Node ID directory of the ftp server
Nothing have been cleaned  
 11.1с - Вывод при ошибке 
Start remove old or excess directories in the Node ID directory of the ftp server
Remove a directory 600
Error !!! You have an error on the ftp server. Check directory name as the node id#2,permissions etc
FTP server have cleaned,bye! 
FTP server have cleaned,bye!

12. ftpold  - отобразит старые или лишние файлы и папки на фтп-сервере (в отношении к Ноде)
пример: ./mgr5back.py ftpold
Start remove old or excess directories in the Node ID directory of the ftp server
Old or excess file or directory 999
Old or excess file or directory 161

13.  ftpdel     - удалить папку или файл на фтп сервере вручную
пример: ./mgr5back.py ftpdel 999
Remove the directory 999
14. zabbix-marks - Create all zabbix marks  
14.1 Можно запускать при стартовой установке или после дебага ошибки, в противном случаи в заббиксе
будет висеть ошибка до следующего запуска бекапа. 
Восстановление 
Заходим на бекап сервер 
1.1 Смотрим куда бекапится:
   grep name `grep ftp_conn /root/scripts/mgr5back/config.ini | awk '{print $2}'`
1.2 На бекап сервере: cd number_of_node/vm-id/date
example: cd /2/229/20170611191737
Разархивировать 
2.1 mv vds vds.gz
example: mv vm15497_20170611191737  vm15497_20170611191737.gz
2.2 Копирование на ноду где будем восстанавливать 
 На ноде 
3.1 Запуск gunzip vds.gz
example: gunzip vm15497_20170611191737.gz 
Заливаем бекап на img c виртуальной машинной: dd if=vds of=/IMG 
Note: Виртуальная машина должна быть выключена, и равного или большего размера бекапа.      
 

