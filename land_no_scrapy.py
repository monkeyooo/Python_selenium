import pytesseract
import matplotlib.pyplot as plt
import cv2
import numpy as np
from selenium import webdriver
import time
import pymysql
import csv
from PIL import Image

# -----------------------------------------------------------main-----------------------------------------------------------
# parameters
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select

account = '89855397'
password = 'a7410852'
hinetLoginUrl = 'https://aaav2.hinet.net/A1/AuthScreen.jsp'
waitTime = 1

driver = webdriver.Chrome('/Users/chuck/Desktop/Work-RMC/Script/chromedriver')
time.sleep(waitTime)
urlLocation = 'https://ep.land.nat.gov.tw/Home/Index'
driver.get(urlLocation)
time.sleep(waitTime)
agreeCheckBox = driver.find_element_by_id('ok')
agreeCheckBox.click()
agreeButton = driver.find_element_by_id('yes')
agreeButton.click()
time.sleep(waitTime)
urlLocation = 'https://ep.land.nat.gov.tw/Login/AAALogin'
driver.get(urlLocation)
time.sleep(waitTime)


# captcha recognize
class image_to_text:
    def __init__(self):
        self.psm_list = [8, 6, 4]
        self.oem_list = [0, 3, 1, 2]
        self.iter_range = 6

    def erode(self, th):
        ret, th = cv2.threshold(th, 15, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((2, 4), np.uint8)
        erosion = cv2.erode(th, kernel, iterations=1)
        ret, th = cv2.threshold(erosion, 0, 255, cv2.THRESH_BINARY_INV)

        return th

    def trans(self, img):
        self.h, self.w, _ = img.shape  # assumes color image
        ans = ''
        for i in range(0, self.iter_range):
            img = self.erode(img)
            for psm in self.psm_list:
                for oem in self.oem_list:
                    boxes = pytesseract.image_to_boxes(img)
                    ans = pytesseract.image_to_string(img, lang='eng',
                                                      config='--psm {} --oem {} -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz012345678'.format(
                                                          psm, oem))  # print identified text
                    if len(ans[:-2]) == 5:
                        return img, ans[:-2], boxes

        return th, ans, boxes


def recognize_text(src):
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)  # 二值化

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # 结构元素
    bin1 = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)  # 开操作

    kernel2 = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # 结构元素
    open_out = cv2.morphologyEx(bin1, cv2.MORPH_OPEN, kernel2)  # 开操作
    cv2.imshow("open_out", open_out)

    cv2.bitwise_not(open_out, open_out)
    textImg = Image.fromarray(open_out)
    res = pytesseract.image_to_string(textImg)
    print(len(res))
    print(res)
    return res


captchaAccept = False
while True:
    accountTextArea = driver.find_element_by_id('aa-uid')
    accountTextArea.send_keys(account)
    passwordTextArea = driver.find_element_by_id('aa-passwd')
    passwordTextArea.send_keys(password)
    captcha = driver.find_element_by_xpath('//*[@id="AAAIden1"]').screenshot('image.png')
    fig, ax = plt.subplots(figsize=(20, 30))
    predicter = image_to_text()
    filename = 'image.png'
    img = cv2.imread(filename)
    img = cv2.resize(img, (1600, 400), interpolation=cv2.INTER_AREA)
    th, text, boxes = predicter.trans(img)
    captchaText = text
    print(captchaText)
    captchaTextArea = driver.find_element_by_name('aa-captchaID')
    captchaTextArea.send_keys(captchaText)
    driver.find_element_by_id('submit_hn').click()
    time.sleep(waitTime)
    try:
        driver.switch_to.alert.accept()
        print("alert accepted")
    except NoAlertPresentException:
        print("no alert")
        captchaAccept = True
        break
    time.sleep(waitTime)
print('Captcha correct : ')
print(captchaAccept)


def getLandInfo(area, street):
    db_settings = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "db": "dragon_info_comp",
        "charset": "utf8"
    }

    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            command = "SELECT * FROM taichung WHERE area LIKE %s AND `section` LIKE %s"
            cursor.execute(command, (area, '%' + street + '%'))
            result = cursor.fetchall()
        # 儲存變更
        print(result)
        return result
    except Exception as ex:
        print(ex)


if captchaAccept:
    driver.get('https://ep.land.nat.gov.tw/EpaperApply/TaiwanMap')
    time.sleep(waitTime)
    dataList = getLandInfo('中區', '繼光段一小段')
    city = '臺中市'
    area = '中區'
    select = Select(driver.find_element_by_id('City_ID'))
    select.select_by_visible_text(city)
    select = Select(driver.find_element_by_id('area_id'))
    select.select_by_visible_text(area)
    main_page = driver.current_window_handle
    print(main_page)
    for landData in dataList:
        dataId = landData[0]
        section_name = '繼光段一小段'
        land_no = landData[3]
        sectionSelectionList = driver.find_elements_by_class_name('session_name')

        for section in sectionSelectionList:
            if section.get_attribute('name') == section_name:
                print(section.get_property('id'))
                element = driver.find_element_by_id(section.get_property('id'))
                driver.execute_script("$(arguments[0]).click();", element)
                break
        time.sleep(waitTime)
        driver.find_element_by_xpath('//*[@id="INPUT_013"]').clear()
        driver.find_element_by_xpath('//*[@id="INPUT_013"]').send_keys(land_no)
        driver.find_element_by_xpath('//*[@id="EdocQryArea"]/a[2]').click()
        print(driver.window_handles)
        if driver.current_window_handle == main_page:
            driver.switch_to.window(driver.window_handles[1])
        time.sleep(waitTime)
        while True:
            try:
                captcha = driver.find_element_by_xpath('//*[@id="ApplyForm"]/img').screenshot('inside.png')
                driver.find_element_by_id('CaptchaValue').clear()
                filename = 'inside.png'
                img = cv2.imread(filename)
                captchaText = recognize_text(img)
                print(captchaText)
                driver.find_element_by_id('CaptchaValue').send_keys(captchaText)
                driver.find_element_by_xpath('//*[@id="ApplyForm"]/input[15]').click()
            except NoSuchElementException:
                print('No captcha')
                break
        try:
            time.sleep(waitTime)
            table = driver.find_elements_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form')
            if len(table) > 0:
                data = str(table[0].text).split("\n")
                data.pop(0)
                print(data)
                if len(data) != 0:
                    with open('test.csv', 'a') as csvFile:
                        for dataInfo in data:
                            writer = csv.writer(csvFile)
                            detail = dataInfo.split(" ")
                            print(detail[0], detail[1])
                            writer.writerow([dataId, detail[0], detail[1]])
                time.sleep(waitTime)
            print('ok')
        except NoSuchElementException:
            print('ok')
        time.sleep(waitTime)
        try:
            driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td/input[2]').click()
        except NoSuchElementException:
            driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td/input').click()
        driver.switch_to.window(main_page)


def updateLandInfo(nantou_id, other_serial_no, owner_name):
    db_settings = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "db": "dragon_info_comp",
        "charset": "utf8"
    }

    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            command = "INSERT INTO nantou_land_info (nantou_id, other_serial_no, owner_name)" \
                      "VALUES(%s, %s, %s)"
            cursor.execute(command, )
            cursor.execute(command, (nantou_id, other_serial_no, owner_name))
        # 儲存變更
        conn.commit()
    except Exception as ex:
        print(ex)

# https://ep.land.nat.gov.tw/Content/ValidateNumber.ashx
