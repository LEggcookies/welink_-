# 中软&sfx WeLink 打卡

### 原理
1. crontab 创建定时任务
2. webdriver 自动点击打卡

### 使用
安装环境
python、appium

下载 打卡.py 及 watch_appium.py 至本地
根据需要，修改caps启动参数及平台

`crontab -e` 打开 crontab 编辑界面，替换 ${PATH} 为本地路径后保存
```
30 8 * * * /usr/local/bin/python3 ${PATH}/打卡.py >> ${PATH}/load.log 2>&1 &
30 20 * * 0,1,2,4,6 /usr/local/bin/python3 ${PATH}/打卡.py >> ${PATH}/load.log 2>&1 &
20 18 * * 3,5 /usr/local/bin/python3 ${PATH}/打卡.py >> ${PATH}/load.log 2>&1 &
*/15 * * * * /usr/local/bin/python3 ${PATH}/watch_appium.py >> ${PATH}/load.log 2>&1 &
```

### 注意事项
1. 将“考勤打卡”添加到日常办公
2. 更换设备需要手动打卡一次，点击设备异常的弹窗
3. iOS 需打开页面至“业务”，杀掉应用后重新打开为业务界面
