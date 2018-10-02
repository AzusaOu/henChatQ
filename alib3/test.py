import acrypt as ct

if __name__ == '__main__':
    pt1 = 'FUCK THE WORLD'.encode('utf-8')
    pt2 = 'ありがとうございます！'.encode('utf-8')
    
    pt1_md5 = ct.str2md5(pt1)
    pt2_md5 = ct.str2md5(pt2)
    print(pt1_md5)
    print(pt2_md5)

    rg = ct.RSAGen(1024)
    pbk, pvk = rg.get()

    ru = ct.RSAUtilize()
    pm1e = ru.encrypt(pbk, pt1_md5)
    pm2e = ru.encrypt(pbk, pt2_md5)
    print(len(pm1e))
    print(len(pm2e))

    print(ru.decrypt(pvk, pm1e))
    print(ru.decrypt(pvk, pm2e))