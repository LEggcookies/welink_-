#! /usr/local/bin/python3
#encoding=utf-8

import time
import appium
import datetime
import random
from appium import webdriver
from chinese_calendar import is_workday

def sxf_is_workday() -> bool:
    date = datetime.datetime.today().date()
    if is_workday(date):
        return True
    else:
        for make_up in make_up_workday_list:
            make_up_date = datetime.datetime.strptime(make_up, '%Y-%m-%d')
            return make_up_date == date
    return False

def and_find_element_by_text(driver, class_type, element_text, timeout=3) -> appium.webdriver.webelement.WebElement:
    '''返回 text element or None'''
    print('获取页面中的所有文本控件')
    for i in range(timeout):
        print(f'第{i}次尝试获取元素: {element_text}')
        item_text = ''
        items = driver.find_elements_by_class_name(class_type)
        print(f'遍历元素，size为: {len(items)}')
        for item in items:
            # 遍历文本控件，寻找可以匹配的文本控件
            try:
                item_text = item.get_attribute('text')
            except Exception as e:
                print(f'获取元素属性失败，原因为：{e}')
            if item_text == element_text:
                print(f'find text: {item_text}, type is {type(item)}')
                return item
        time.sleep(1)
    return None

def and_clock_in(deviceName,platformVersion):
    caps = {
    "appium:deviceName": deviceName,
    "platformName": "Android",
    "appium:platformVersion": platformVersion,
    "appium:appPackage": "com.huawei.welink",
    "appium:appActivity": "huawei.w3.ui.welcome.W3SplashScreenActivity",
    "appium:noReset": True
    }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps) # 启动app
    time.sleep(5)
    clock_in_btn = and_find_element_by_text(driver,'android.widget.TextView',"考勤打卡")
    if clock_in_btn:
        print('找到考勤打卡按钮')
        clock_in_btn.click() # 点击

        time.sleep(5)
        clock_in_btn = and_find_element_by_text(driver,'android.view.View',"打卡")
        if clock_in_btn:
            print('找到打卡按钮')
            clock_in_btn.click() # 点击
            result = and_find_element_by_text(driver,'android.view.View',"打卡成功")
            if result:
                time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'打卡成功，打卡时间为 {time1}')
                return True

    time2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'打卡失败，打卡时间为 {time2}')
    return False

def ios_clocl_in(udid,platformVersion):
    caps = {
        "appium:deviceName": "iPhone",
        "platformName": "iOS",
        "appium:platformVersion": platformVersion,
        "appium:app": "com.huawei.cloudlink.workplace",
        "appium:udid": udid,
        "appium:noReset": False
    }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps) # 启动app
    time.sleep(5)
    # JavascriptExecutor js = (JavascriptExecutor)driver
    # js.executeScript("mobile: pressButton", ImmutableMap.of("name","home"))
    driver.execute_script("mobile: pressButton", ImmutableMap.of("name","home"))

    clock_in_btn = driver.find_element_by_ios_predicate("name == '考勤打卡'")
    if clock_in_btn:
        print('找到考勤打卡按钮')
        clock_in_btn.click() # 点击

        time.sleep(5)
        clock_in_btn = driver.find_element_by_ios_predicate("name == '打卡'")
        # clock_in_btn = driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="打卡"]')
        print(clock_in_btn)
        if clock_in_btn:
            print('找到打卡按钮')
            clock_in_btn.click() # 点击
            time.sleep(5)
            result = driver.find_element_by_ios_predicate("name == '打卡成功'")
            if result:
                time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'打卡成功，打卡时间为 {time1}')
                return True

    time2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'打卡失败，打卡时间为 {time2}')
    return False
    

if __name__ == "__main__":

    # 需修改参数
    platformName = 'Android'
    udid = ''
    platformVersion = '10'

    make_up_workday_list = ['2022-01-08','2022-02-12','2022-03-05','2022-04-09','2022-05-14','2022-06-11','2022-07-02','2022-08-06','2022-09-03','2022-10-08','2022-11-05','2022-12-03']

    is_workday = sxf_is_workday()
    if not is_workday:
        print('不是工作日，不需要打卡')
    else:
        print('是工作日，开始打卡')
        sleep_time = random.randint(0,1800)  # 30分钟内随机
        print(f'sleep {sleep_time}s 后正式启动打卡流程')
        time.sleep(sleep_time)
        
        if platformName == 'Android':
            and_clock_in(udid,platformVersion)
        elif platformName == 'iOS':
            ios_clocl_in(udid,platformVersion)
        else:
            print('打卡失败，不支持的平台')