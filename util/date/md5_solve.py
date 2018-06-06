# coding=utf-8
import hashlib
import base64


def decryptMD5(testHash):
    s = []
    while True:
        m = hashlib.md5()
        for c in s:
            m.update(chr(c))
        hash = m.hexdigest()
        if hash == testHash:
            return ''.join([chr(c) for c in s])
        wrapped = True
        for i in range(0, len(s)):
            s[i] = (s[i] + 1) % 256
            if s[i] != 0:
                wrapped = False
                break
        if wrapped:
            s.append(0)


def md5(pwd):
    m = hashlib.md5()
    m.update(pwd.encode("utf-8"))
    return m.hexdigest()


def b64(pwd):
    pwd = bytes(pwd, encoding="utf8")
    base = base64.b64encode(pwd)
    return str(base, encoding="utf-8")


if __name__ == "__main__":
    tmp = "2211252428@qq.com" + "0755a07db45e9bfa0e96e03c76d107d9" + "dNgrIBwedcfrfosFislkkwwTgaDffllpo"
    print(tmp)
    tmp = md5(tmp)
    tmp = b64(tmp)
    print(tmp[0:-3])
