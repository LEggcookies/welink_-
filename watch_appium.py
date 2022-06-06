import os,time,subprocess
def watch_appium():
    str = os.popen("/usr/sbin/lsof -i:4723|grep 4723").read()
    result = str.replace(" ","").replace("\n","")
    return result

if __name__ == "__main__":
    commond_and="/usr/local/bin/node /Applications/Appium\ Server\ GUI.app/Contents/Resources/app/node_modules/appium/build/lib/main.js -p 4723"
    if '4723' not in watch_appium():
       print("appium for and is not running,start runing")
       subprocess.Popen(commond_and,shell=True)
       print("appium for and is running")