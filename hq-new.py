#-*-coding:utf-8-*-

import sys
import pickle

import alib3.acrypt as acrypt

if __name__ == '__main__':
    username = sys.argv[1].encode('utf-8')
    if len(username) > 16:
        print('Username should not longer than 10')
    server = sys.argv[2]
    port = int(sys.argv[3])
    timeout = int(sys.argv[4])
    print('Generating RSA keys...')
    r = acrypt.RSAGen(2048)
    pbk, pvk = r.get()

    J = {
        'server': server,
        'user': username,
        'port': port,
        'timeout': timeout,
        'pbk': pbk,
        'pvk': pvk
    }
    pickle.dump(J, open('user.conf', 'wb'))
    
    print('New user created.')