# coding=utf-8

import inspect


def module_c_fun():
    print("call {0}".format(inspect.stack()[0][3]))


if __name__ == "__main__":
    moule_c_fun()
