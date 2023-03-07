# -*- coding: UTF-8 -*-
import os, config, utils, pexpect, time, sys

# 批量生成jks
# 开始创建需要的文件夹
import random
import string

if config.__random_package:
    utils.mkdirs_with_package()
else:
    utils.mkdirs()
# 创建需要的保存jks信息的txt
utils.creat_jksinfos()
for _dir in os.listdir(utils._jks_file_):
    _file_path = utils._jks_file_ + "/" + _dir + "/" + config.__keystore
    if config.__random_alias:
        alias = ''.join(random.sample(string.ascii_lowercase, 3))
    else:
        alias = config.__alias
    _shell_genkey = "keytool -genkey -v -keystore " + _file_path \
                    + " -alias " + alias + " -storepass " + config.__storepass \
                    + " -keypass " + config.__keypass + " -keyalg " + config.__keyalg \
                    + " -keysize " + str(config.__keysize) + " -validity " + str(config.__validity)
    print("ready to execute cdmstr : " + _shell_genkey)
    # 交互输入开始
    child = pexpect.spawn(_shell_genkey, encoding="UTF-8")
    child.expect("您的名字与姓氏是什么")
    if config.__random_package:
        child.sendline(_dir)
    else:
        child.sendline(config.__owner)
    child.expect("您的组织单位名称是什么")
    child.sendline(config.__comp_subname)
    child.expect("您的组织名称是什么")
    child.sendline(config.__comp_name)
    child.expect("您所在的城市或区域名称是什么")
    child.sendline(config.__comp_location)
    child.expect("您所在的省/市/自治区名称是什么")
    child.sendline(config.__comp_location)
    child.expect("该单位的双字母国家/地区代码是什么")
    child.sendline(config.__comp_code)
    child.expect("是否正确")
    child.sendline("y")
    print("jks path : " + _file_path)
    print("waitting for the job done....")
    # 休眠等待文件生成
    time.sleep(2)
    print("move to pkcs12")
    # 迁移行业标准pkcs12
    _shell_pkcs12 = "keytool -importkeystore -srckeystore " + _file_path + " -destkeystore " + _file_path + " -deststoretype pkcs12"
    pkcs12 = pexpect.spawn(_shell_pkcs12, encoding="UTF-8")
    pkcs12.expect("输入源密钥库口令")
    pkcs12.sendline(config.__keypass)
    # 休眠等待文件生成
    time.sleep(1)
    # 删除旧的jks
    utils.deleteOldJKS(_file_path + ".old")
    print("done!")

# 不需要md5&sha1&sha256不执行
if not config.__jks_info:
    print("all jks ready!enjoy")
    sys.exit(0)

for _dir in os.listdir(utils._jks_file_):
    print("start query md5 & sha1 & sha256 ...")
    # 所在文件夹
    _jks_dir = utils._jks_file_ + "/" + _dir
    # jks文件路径
    _jks_file = _jks_dir + "/" + config.__keystore
    # jksinfo文件路径
    _jks_info_dir = _jks_dir + "/" + utils._jks_info_
    _shell_list = "keytool -v -list -keystore " + _jks_file
    list = pexpect.spawn(_shell_list, encoding="UTF-8")
    list.expect("密钥库口令")
    list.sendline(config.__keypass)
    utils.writeJKSInfo(list.read(), _jks_info_dir)
    pass

print("all jks ready!enjoy")
sys.exit(0)
