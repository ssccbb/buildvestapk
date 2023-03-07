import os
import subprocess
import constants
from plugin.APKPlugin import APKPlugin
from plugin.ZipPlugin import ZipPlugin

if __name__ == '__main__':
    dirs = os.path.join(constants.path_self, "test")
    apk_path = subprocess.check_output(f'find {dirs} -name *.apk', shell=True).decode('UTF-8').strip()
    apk_name = subprocess.check_output(f'find {dirs} -name *.apk|cut -d/ -f8', shell=True).decode('UTF-8').strip()
    print(f'apk_path={apk_path}')
    print(f'apk_name={apk_name}')
    # APKPlugin.unzip_apk_file(apk_path, apk_path.replace(".apk", "_apktool"))
    ZipPlugin.un_zip_file(apk_path, apk_path.replace(".apk", "_zip"))
    dex_path = subprocess.check_output(f'find {dirs} -name *.dex', shell=True).decode('UTF-8').strip()
    for dex in dex_path.split('\n'):
        print(f'dex_path={dex}')
        APKPlugin.change_dex_to_jar(dex, dex.replace('.dex', '.jar'))
