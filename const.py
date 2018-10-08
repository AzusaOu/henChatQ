class PATH:
    SETTING_SERVER = 'server.json'
    PATH_FRIENDS = './friends/'
    PATH_USER = 'user.conf'
    INFO_CHANNELS = 'channels.json'

class API_CMD_IN:
    ONLINE = 0x00
    NEWUSER = 0x01
    SEND = 0x02
    LISTEN = 0x03

class API_CMD_OUT:
    LOGIN = 0x00
    TEXTMSG = 0x01

class RX_CMD:
    MSG = 0x04

class STYPE:
    PLAINTEXT = b'\x00'
    FILE = b'\x01'
    FOLLOW = b'\x02'