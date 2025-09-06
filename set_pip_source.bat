@echo off

REM 创建pip配置目录
if not exist "%USERPROFILE%\pip" mkdir "%USERPROFILE%\pip"

REM 设置华为pip源
echo [global] > "%USERPROFILE%\pip\pip.ini"
echo index-url = https://repo.huaweicloud.com/repository/pypi/simple/ >> "%USERPROFILE%\pip\pip.ini"
echo trusted-host = repo.huaweicloud.com >> "%USERPROFILE%\pip\pip.ini"

echo 华为pip源设置成功！