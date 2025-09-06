import os
import sys

# 获取用户目录
user_profile = os.environ.get('USERPROFILE', '')
if not user_profile:
    print('无法获取用户目录')
    sys.exit(1)

# 创建pip配置目录
pip_dir = os.path.join(user_profile, 'pip')
if not os.path.exists(pip_dir):
    os.makedirs(pip_dir)
    print(f'创建pip配置目录: {pip_dir}')

# 创建pip.ini文件
pip_ini_path = os.path.join(pip_dir, 'pip.ini')
with open(pip_ini_path, 'w', encoding='utf-8') as f:
    f.write('[global]\n')
    f.write('index-url = https://repo.huaweicloud.com/repository/pypi/simple/\n')
    f.write('trusted-host = repo.huaweicloud.com\n')

print(f'华为pip源已成功设置，配置文件位于: {pip_ini_path}')