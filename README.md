# iconTestnetTracker
Django framework, python required

__added iconloop SDK required__

## Docker image
```bash
- docker pull perfectr2/icon-testwebapp
- docker run -it -p 8000:8000 -p 9000:9000 --rm perfectr2/icon-testwebapp:latest
# cd /work/djangoApp/iconTestnetTracker
# service mysql start
# python3 manage.py runserver 0.0.0.0:8000
```

## Python Version
> Python 3.7.3

## MySQL DB

```
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Server version          10.1.38-MariaDB-0+deb9u1
Protocol version        10
Connection              Localhost via UNIX socket
UNIX socket             /var/run/mysqld/mysqld.sock
```
## pip list
> require pip install -r requirements.txt

```bash
foo@bar:~$ pip install -r requirements.txt

Package                 Version    
----------------------- -----------
aio-pika                3.0.1      
aiofiles                0.4.0      
aiohttp                 3.4.4      
async-timeout           3.0.1      
attrs                   19.1.0     
backcall                0.1.0      
beautifulsoup4          4.7.1      
certifi                 2019.3.9   
cffi                    1.12.3     
chardet                 3.0.4      
click                   6.7        
coloredlogs             10.0       
cytoolz                 0.9.0.1    
decorator               4.4.0      
Django                  2.2.1      
django-ipware           2.1.0      
django-mathfilters      0.4.0      
earlgrey                0.0.4      
eth-hash                0.2.0      
eth-keyfile             0.5.1      
eth-keys                0.2.2      
eth-typing              2.1.0      
eth-utils               1.6.0      
funcsigs                1.0.2      
future                  0.16.0     
geoip2                  2.9.0      
grpcio                  1.19.0     
grpcio-tools            1.19.0     
gunicorn                19.9.0     
httptools               0.0.13     
humanfriendly           4.18       
iconcommons             1.0.5.2    
iconrpcserver           1.3.0      
iconsdk                 1.0.9      
iconservice             1.3.0      
idna                    2.8        
ipython                 6.4.0      
ipython-genutils        0.2.0      
jedi                    0.13.3     
jsonrpcclient           2.6.0      
jsonrpcserver           3.5.6      
jsonschema              2.6.0      
maxminddb               1.4.1      
msgpack                 0.6.1      
multidict               4.5.2      
multipledispatch        0.5.0      
mysqlclient             1.4.2.post1
parso                   0.4.0      
pexpect                 4.7.0      
pickleshare             0.7.5      
pika                    0.12.0     
pip                     19.1.1     
plyvel                  1.0.5      
prompt-toolkit          1.0.16     
protobuf                3.7.0      
ptyprocess              0.6.0      
pycparser               2.19       
pycryptodome            3.8.2      
pygeoip                 0.3.2      
Pygments                2.4.2      
pytz                    2019.1     
requests                2.22.0     
sanic                   18.12.0    
Sanic-Cors              0.9.6      
Sanic-Plugins-Framework 0.7.0      
secp256k1               0.13.2     
setproctitle            1.1.10     
setuptools              41.0.1     
shortuuid               0.5.0      
simplegeneric           0.8.1      
six                     1.12.0     
soupsieve               1.9.1      
sqlparse                0.3.0      
tbears                  1.2.0      
toolz                   0.9.0      
traitlets               4.3.2      
ujson                   1.35       
urllib3                 1.25.3     
uvloop                  0.12.2     
wcwidth                 0.1.7      
websockets              6.0        
wheel                   0.33.1     
yarl                    1.3.0 
```
