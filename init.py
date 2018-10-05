#-*-coding:utf-8-*-

import sys
import pickle

import alib3.acrypt as acrypt

def initNew(username):
    if len(username) > 16:
        print('Username should not longer than 16')

    print('Generating RSA keys...')
    r = acrypt.RSAGen(2048)
    pbk, pvk = r.get()

    J = {
        'user': username,
        'pbk': pbk,
        'pvk': pvk
    }
    pickle.dump(J, open('user.conf', 'wb'))
    
    print('New user created.')

if __name__ == '__main__':
    username = sys.argv[1].encode('utf-8')
    initNew(username)