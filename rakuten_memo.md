# Rakuten memo

## small points
* change bash
```
chsh -s /bin/bash
```
  
* CPU
```
cat /proc/cpuinfo | grep 'core id' |wc -l
```
 
* メモリ
```
/proc/meminfo
awk '$3=="kB"{if ($2>1024**2){$2=$2/1024**2;$3="GB";} else if ($2>1024){$2=$2/1024;$3="MB";}} 1' /proc/meminfo | column -t
```
  
* add user
```
groupadd -g 20500 clx_support
useradd -u 20500 -g 20500 -m -d '/home/clx_support' -s '/bin/bash' -p '$1$clx_supp$y5tkVcQlvhYRZGAFp.aFA.' clx_support
```

* change global variables
```
show GLOBAL variables like '%session_log_slow_queries%';
SET GLOBAL session_log_slow_queries = false;
```
 
* change global variables data protection time
```
mysql > SHOW GLOBAL VARIABLES LIKE '%rebalancer_reprotect_queue_interval_s%';
mysql > SET GLOBAL rebalancer_reprotect_queue_interval_s=5400;
```

* run query in command line
```
mysql -h host -u root -proot -e "show databases;";
```
  
* change timezone of db
```
SET GLOBAL system_time_zone='Asia/Tokyo'
SHOW GLOBAL VARIABLES LIKE '%time_zone%';
```
 
* rename database name
```
echo "show tables" |mysql -N kyo2 |awk '{print "rename table kyo2."$1" to kyo."$1";"}'|mysql kyo -vvv
rename table currentdb.t1 to newdb.t1;
```
 
* Cloning a MySQL database on the same MySql instance
```
mysqldump db_name | mysql new_db_name
```

* drop user
```
cat /tmp/drop_empty_user_stg.txt | awk '{print "DROP USER "$1";"}'|mysql -vvv
```
  
* zip/unzip
```
tar czvf hoge.tar.gz hoge1 hoge2 ... //圧縮
tar xzvf hoge.tar.gz //解凍
```
  
* check file size
```
du -hs ./*
```

* systemd
```
systemd
display all registered unit
systemctl list-unit
journalctl --since "2017-01-01 00:00:00"
→ /var/log/messages
systemctl --system list-timers
  
systemctl daemon-reload
 
systemctl enable /etc/systemd/system/minute-timer.timer
systemctl start  /etc/systemd/system/minute-timer.timer
 
systemctl enable /etc/systemd/system/testservice.service
  
systemctl is-active clustrix-backup.service
systemctl status clustrix-backup.service
systemctl list-unit-files
```

* create file with today's date
```
vi /etc/ssh/sshd_config.`date +\%Y\%m\%d`
```

* collect clustrix log
```
collect log from clustrix
/opt/clustrix/bin/clx cmd 'grep "^2017-02-10 04" /data/clustrix/log/clustrix.log' > /tmp/cl_2017-02-10.out
scp cl_2017-02-10.out xuyulian01@loginjp201z.prod.jp.local:/home/xuyulian01
scp xuyulian01@loginjp201z.prod.jp.local:/home/xuyulian01/cl_2017-03-28.out /Users/yulian.xu/Documents/
```

* How can I use grep to find a word inside a folder?
```
grep -nr 'yourString*' .
  
-n            Show relative line number in the file
'yourString*' String for search, followed by a wildcard character
-r            Recursively search subdirectories listed
.             Directory for search (current directory)
```

* add index
```
add index
ALTER TABLE テーブル名 ADD INDEX インデックス名(カラム名);
  
drop index
ALTER TABLE テーブル名 DROP INDEX インデックス名;
```

* session stuck issue
```
select holder, waiter cnt FROM system.lockman ORDER BY cnt desc;
SELECT * FROM system.sessions WHERE xid = 6388237304741126148\G
```

* passwordless authentication
```
mkdir .ssh
 
ssh-keygen
 
scp ~/.ssh/id_rsa.pub xuyulian01@dm-mars106.prod.jp.local:/home/xuyulian01/.ssh/id_rsa_loginjp201z.pub
 
 
cat ~/.ssh/id_rsa_loginjp201z.pub >> ~/.ssh/authorized_keys
```

* umount volume
```
#umount directory
umount <dir>
  
#check if device is being used
lsof | grep <keyword>
  
#if device is busy
umount -l <dir>
  
#copy fstab
cp -pr /etc/fstab
  
#vifstab
vi /etc/fstab
  
#delete unnessary part in case of auto mount
```

* use dell om tool to check memory status
```
/opt/dell/srvadmin/bin/omreport chassis memory
```

* check default gateway
```
[root@asplunksrch211z ~]# netstat -rn
 
Kernel IP routing table
 
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
 
100.71.27.0     0.0.0.0         255.255.255.0   U         0 0          0 eth1
 
169.254.0.0     0.0.0.0         255.255.0.0     U         0 0          0 eth1
 
0.0.0.0         100.71.27.254   0.0.0.0         UG        0 0          0 eth1
```

* edit prompt
```
PS1='[\u@\h: \t \W]\$ ' ; export PS1
```

* [share public key](https://qiita.com/kentarosasaki/items/aa319e735a0b9660f1f0)
 ``` 
for i in `cat /tmp/stglist`; do ssh-copy-id xuyulian01@$i; done
```
* check clustrix db size
```
Database size(v7)
SELECT Database, SUM(bytes)/1024/1024/2 AS MB FROM system.table_sizes WHERE `Database`='<db_name>';
Table size(v7)
SELECT `Table`, SUM(bytes)/1024/1024/2 AS MB FROM system.table_sizes WHERE `Database`='<db_name>' AND `Table`='<table_name>';
order by database size
SELECT Database, SUM(bytes)/1024/1024/2 AS MB FROM system.table_sizes group by Database order by MB desc;
```

* how to do mysqldump
```
mysqldump --single-transaction --user="root" --password="" --host="stg-dclx-jupiter-v.stg.jp.local" --port=3306 --databases research_racross3 > research20161011-02.dat&
```

* check backup process
```
select * from system.backup_status\G
#If restore task exsit?
 
select bytes / expected_bytes * 100 from system.backup_status;
#Checkout if the db size is growing?
```

* confirm disk status after disk replacement(dell)
```
/opt/dell/srvadmin/bin/omreport storage pdisk controller=0
/opt/dell/srvadmin/bin/omreport storage vdisk controller=0
```

* restore database as another identifier from Azure
```
# mysql -h stg-dm-planet405z.stg.jp.local -u root -psroot -e "RESTORE point_campaign_test AS point_campaign_test_2 FROM 'ftp://anonymous:anonymous@100.77.16.5/stg-jupiter-201702/05/full/point_campaign_test.224630'"
```

* Move original tables to another db (point_campaign_test TO point_campaign_test_3)
```
mysql> create database point_campaign_test_3
mysql> echo "show tables" |mysql -N point_campaign_test |awk '{print "rename table point_campaign_test."$1" to point_campaign_test_3."$1";"}'|mysql point_campaign_test_3 -vvv
```

* Move restored table to original db(point_campaign_test_2 TO point_campaign_test)
```
mysql> echo "show tables" |mysql -N point_campaign_test_2 |awk '{print "rename table point_campaign_test_2."$1" to point_campaign_test."$1";"}'|mysql point_campaign_test -vvv
```

* how to configure bond
```
cd /etc/sysconfig/network-scripts
nmtui
nmcli c add type bond ifname bond1 con-name bond1 mode balance-alb
nmcli c s
nmcli c mod bond1 ipv4.method disabled ipv6.method ignore
nmcli c s
nmcli c add type bond-slave ifname enp134s0f0 con-name bond-slave-enp134s0f0 master bond1
nmcli c s
nmcli c add type bond-slave ifname enp134s0f1 con-name bond-slave-enp134s0f1 master bond1
nmcli c s
nmcli c add type vlan ifname bond1.1648 con-name bond1.1648 dev bond1 id 1648
nmcli c s
nmcli c mod bond1.1648 ipv4.method manual ipv4.address "100.66.34.99/24"
nmcli c sh
 
cat /proc/net/bonding/bond1
cat /etc/sysconfig/network-scripts/ifcfg-bond-bond1
systemctl restart network
 
timedatectl set-timezone Asia/Tokyo
```

* pyenv
```
python -V
which python
pyenv versions
pyenv global 3.6.3
mkdir /Users/yulian.xu/Documents/code/venv/monitoring
source monitoring/bin/activate
python -m venv /Users/yulian.xu/Documents/code/venv/monitoring
source monitoring/bin/activate
 
deactivate
pyenv global 2.7.13
virtualenv /Users/yulian.xu/Documents/code/venv2/monitoring
source monitoring/bin/activate
```

python unit test
```
python -m unittest tests.test_utils
```

* impressive mail template
```
資料ありがとうございます。拝見させていただきます。
お手数ですが既存サーバの構成（スペック）をご共有頂けると幸いです。
現在のDBサーバのHW構成は以下のとおりです。
---
CPU:
  インテル Xeon E5-2630 v3 2.4GHz,20M キャッシュ,8.00GT/s QPI,ターボ,HT,8C/16T: 2ソケット
Memory:
  16GB RDIMM, 2400MT/s, デュアルランク, x8 データWidth: 8本
クエリログ含むログ領域(Bin Log除く)
  1.8TB 10K RPM SAS 12Gbps 512e 2.5インチ ホットプラグ ハードドライブ: 2本(ミラーリング)
OS & Data Disk:
  3.84TB ソリッドステート ドライブ SAS Mix Use MLC 12Gbps 2.5インチ ホット プラグドライブ: 8本(Raid-10)
Raid Card:
  PERC H730P 内蔵 RAID コントローラ, 2GB キャッシュ: 1つ
NIC:
  QLogic 57800S 2x10Gb DA/SFP+ + 2x1Gb BT ネットワーク ドーターカード(SFP+ Optics/DA ケーブルなし): 1つ
---
加えて、検証機をお借りしようかという話になったSplunkのサーバについてですが、現状使用しているサーバのスペックは以下のとおりです。こちらのついては性能面での課題はありませんので、現行世代の各種コンポーネントを使用した形のスペックで弊社DCで検証ができれば助かります。
合わせて、こちらのサーバについては見積もりを出していただくことは可能でしょうか? 現状供給いただいているDellさんのサーバと価格比較させていただきます。
---
CPU:
  インテル Xeon E5-2630 v4 2.2GHz,25M キャッシュ,8.0 GT/s QPI,ターホ ,HT,10C/20T (85W) Max Mem 2133MHz: 2ソケット
Memory:
  8GB RDIMM, 2400MT/s, シングルランク, x8 データ Width: 8本
OS Disk:
  200GB SATA SSD Write Intensive, 2.5", 6Gbps, HotPlug: 2本(ミラーリング)
Data Disk:
  1.6TB SATA SSD Read Intensive MLC, 2.5", 6Gbps, HotPlug: 8本(Raid-6)
Raid Card:
  PERC H730 内蔵 RAID コントロ-ラ, 1GB キャッシュ: 1つ
NIC:
  QLogic 57800S 2x10Gb DA/SFP+ + 2x1Gb BT ネットワーク ドーターカード(SFP+ Optics/DA ケーブルなし): 1つ
---
スペックに関して以下補足です。
・DBサーバ、Splunk両方共NICに1Gbpsのポートを積んでおりますが、次回購入する際には1Gbpsをあえて入れる必要はありません、
・SplunkのDataディスクとしてRead IntensiveのSSDを積んでおりますが、これは単純に安かったからという理由です、Mix Useで低価格なSSDがあるならそれに越したことはありません。
・それ以外の部分については提示したスペックを踏襲いただければと思います。
以上、よろしくお願い致します。
```
