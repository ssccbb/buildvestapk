# -*- coding: utf-8 -*-
import os

print("-----------------------------")

# 需要的jks数量
__jks_number = 20
# 是否需要生成jksinfo.txt保存md5等相关信息
__jks_info = True
# 是否需要自动随机生成包名
__random_package = True

print("need number : " + str(__jks_number))
print("need jksinfo.txt : " + str(__jks_info))
print("need random package : " + str(__random_package))

__dir = os.path.abspath(".")
# keystore：设置生成的文件名称，包含后缀
__keystore = "yr_release_key.jks"
# alias：设置别名
__alias = "yr"
# storepass：设置文件的密码
__storepass = "LS880617!@#"
# keypass：设置key的密码
__keypass = "LS880617!@#"
# keyalg：设置使用的加密算法，一般写RSA
__keyalg = "RSA"
# keysize：指定密钥长度（默认 1024）
__keysize = 2048
# validity：设置有效期（天）
__validity = 25 * 365

print("jks root : " + __dir)
print("jks name : " + __keystore)
print("jks alias : " + __alias)
print("jks storepass : " + __storepass)
print("jks keypass : " + __keypass)
print("jks keyalq : " + __keyalg)
print("jks keysize : " + str(__keysize))
print("jks validity : " + str(__validity))

# 额外拥有者用户名
__owner = "KQ"
# 额外组织单位名称
__comp_subname = "KQ"
# 额外组织名称
__comp_name = "KQ"
# 额外信息地址
__comp_location = "HZ"
# 额外信息国家代码
__comp_code = "CN"

print("company : " + __comp_name)
print("company location : " + __comp_location)
print("location code : " + __comp_code)

print("-----------------------------")
print("config ready...")
