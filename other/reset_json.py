# coding=utf-8
import os

import constants


def delete_map_key():
    """
    处理mapkey
    :return:
    """
    backup_file = os.path.join(constants.path_self, "backup.json")
    with open(backup_file, mode='r') as f:
        lines = f.readlines()
        f.close()
    with open(backup_file, mode='w') as f:
        for line in lines:
            if "mapKey" not in line:
                f.writelines(line)
        f.close()


def add_boolean_key():
    """
    处理缺失值
    :return:
    """
    backup_file = os.path.join(constants.path_self, "backup.json")
    with open(backup_file, mode='r') as f:
        lines = f.readlines()
        f.close()
    with open(backup_file, mode='w') as f:
        for line in lines:
            if "hideTeen" in line and not line.strip().endswith(","):
                f.writelines(line + ",")
                f.writelines("\"hideDialog\":\ttrue,\n")
                f.writelines("\"hidePermissionDialog\":\ttrue\n")
            else:
                f.writelines(line)
        f.close()

# delete_map_key()
# add_boolean_key()
