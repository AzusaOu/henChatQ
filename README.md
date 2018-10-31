# henChatQ

**henChatQ** is a simplified communication application without a customized server. It is based on MQTT protocol, and can send/receive messages to/from any MQTT broker deployed on the Internet.

## Quick start ##
There are two ways to launch henChatQ:
### Executable file ###
Download correct version in the [Release](https://github.com/AzusaOu/henChatQ/releases). Simply type `./henChat`. If it is your first time, the program would guide you to create a new user.  
Executable file is packed by [PyInstaller](https://github.com/pyinstaller/pyinstaller).
### Run the source code ###
Since the program is written in Python 3.6, you need Python 3 environment, as well as these libs (can be installed via pip):

* paho-mqtt
* pycryptodome
* rsa
* websocket-client

Simply install these libraries with `pip3 install -r require.txt`. And then, `python3 henChatQ.py`.

## Safety issue ##
Messages that HCQ sends/receives looks like this:

```
------------------ AES-256 (PSK) ---------------------
| +----+----+----+----+--------+--------------------+|
| | id |time|sign|type|addition|      payload       ||
| +----+----+----+----+--------+--------------------+| => GZIP
|   32   10  256   1      32             x           |
------------------------------------------------------
```
* id: name of the sender, len = 32
* time: time stamp of the message, len = 10
* sign: of md5(timestamp + payload), len = 256
* type: type of the message, len = 1  
  0x00 - plain text  
  0x01 - file
* addition: reserve space, len = 32
* payload: body of the message

Safety of the message is insured by pre-shared key (PSK). Users should share the key in other ways. 