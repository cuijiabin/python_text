# coding=utf-8
import hashlib

import string


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


if __name__ == "__main__":
    print(decryptMD5("47bce5c74f589f4867dbd57e9ca9f808"))  # 要破解的md5值，此处为明文test的md5值
