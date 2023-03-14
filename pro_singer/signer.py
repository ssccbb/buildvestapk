import os, sys, shutil

if __name__ in "__main__":
    size = len(sys.argv)
    print(f'{size}')
    apk_file = None
    jks_file = None
    jks_password = None
    jks_alias = None
    if size == 3:
        apk_file = sys.argv[1]
        jks_file = sys.argv[2]
        jks_password = f'LS880617\!@#'
        jks_password = f'yr'
    elif size == 5:
        apk_file = sys.argv[1]
        jks_file = sys.argv[2]
        jks_alias = sys.argv[3]
        jks_password = sys.argv[4]
        # if '!' in str(jks_password):
        #     jks_password = str(jks_password).replace('!', '\!')
    else:
        print(f'use command -->> python3 signer.py [apk] [jks] [alias] [password]')
        exit(-1)

    if apk_file is None or jks_file is None or jks_password is None:
        print(f'use command -->> python3 signer.py [apk] [jks] [password]')
        exit(-1)
    signer_apk_file = apk_file.replace(".apk", "_sign.apk")
    shutil.copyfile(apk_file, signer_apk_file)
    print("开始为apk签名...")
    cmd_signer = f'java -jar /Users/sung/sung/pycharm-projects/buildvestapk/jar/apksigner.jar ' \
                 f'-keystore {jks_file} -alias {jks_alias} -pswd {jks_password} -aliaspswd {jks_password} {signer_apk_file}'
    if os.system(cmd_signer) == 0:
        print("成功为apk签名")
        os.remove("sign.db")
    else:
        raise Exception("apk签名失败")
