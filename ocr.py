import sys
import cv2
import pytesseract
import numpy as np
from PIL import Image


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


# 網路提供之簡易驗證碼驗證
def recognize_text(src):
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)  # 二值化

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # 結構元素
    bin1 = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)  # 操作

    kernel2 = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # 結構元素
    open_out = cv2.morphologyEx(bin1, cv2.MORPH_OPEN, kernel2)  # 操作
    cv2.imshow("open_out", open_out)

    cv2.bitwise_not(open_out, open_out)
    textImg = Image.fromarray(open_out)
    res = pytesseract.image_to_string(textImg)
    return res


def main(argv):
    ocrType = argv[1]
    filename = argv[2]
    if ocrType == '0':
        predicter = image_to_text()
        img = cv2.imread(filename)
        img = cv2.resize(img, (1600, 400), interpolation=cv2.INTER_AREA)
        th, text, boxes = predicter.trans(img)
        captchaText = text
    else:
        captchaText = recognize_text(filename)
    print(captchaText)


main(sys.argv)
