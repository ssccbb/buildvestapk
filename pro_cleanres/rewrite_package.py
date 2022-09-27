import os
from plugin.RewritePackage import *

# 重命名java代码包路径
if __name__ == '__main__':
    # 必须以com文件夹开始处理
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/app")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/library-beauty")
    work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/library-commonlib")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/library-eventbus")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/library-im")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/module-community")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/module-ext")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/module-live")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/module-message")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/module-party")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/module-vchat")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/YR-Network")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/YR-Player")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/YR-SvgaImage")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/YR-Tools")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/YR-Uikit")
    # work_path = os.path.join(constants.path_root, "flutter-project/huajian-android/commonlibrary")
    helper = RewritePackage(work_path)
    print(f'总共 {helper.dir_count} 个包路径,预生成 {len(helper.name)} 个随机备用名')
    # step 1 记录文件结构
    helper.record_file_struct(helper.path)
    print(f'待处理的文件总共 {helper.file_count} 个')
    # step 2 修改包路径
    helper.rename_dir(helper.path)
    print(f'修改包路径完成，开始配对新旧包路径...')
    # step 3 记录修改后的包对应路径
    helper.record_file_struct_after_edit(helper.path)
    # step 4 修改文件内容
    print(f'开始修改文件内包路径引用')
    helper.rename_file(helper.path)
    # step 5 修改清单文件定义的activity路径
    print(f'开始处理清单文件')
    helper.rename_mainfest_content()
    # step 6 修改xml内使用到的自定义view
    helper.rename_layout_content()
    print(f'操作成功！')
