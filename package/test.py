# coding=utf-8

import module_a as ma
import package_bc.module_c
import package_bc.module_b as mb
import package_bc.package_sub.module_s as ms
import package_de

if __name__ == "__main__":
    ma.module_a_fun()
    mb.module_b_fun()
    package_bc.module_c.module_c_fun()
    ms.module_s_fun()
    package_de.module_d.module_d_fun()
    package_de.module_e_fun()
