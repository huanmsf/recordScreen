# coding=utf-8
# 录屏脚本
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from PIL import ImageGrab, Image
from skimage.measure import compare_ssim
import cv2, time, pyautogui as pag, webbrowser, threading, sys

running = True
playing = True
is_test = True
start_time = time.time()
m = PyMouse()
k = PyKeyboard()

# 课程的地址列表
# https://edu.aqniu.com/course/83/task/19741/show
# https://edu.aqniu.com/course/83/task/19747/show
courseUrlList = [
    "https://edu.aqniu.com/course/83/task/19741/show",
    "https://edu.aqniu.com/course/83/task/19747/show",
    "https://edu.aqniu.com/course/83/task/19753/show"
]


# 全屏
def full_screen():
    m.click(800, 500, 1, 2)
    switch_record_status()


# 退出全屏
def un_full_screen():
    switch_record_status()
    time.sleep(2)
    m.click(800, 500, 1, 2)


# 移动进度条到开始播放的位置
def to_start():
    time.sleep(2)
    m.click(10, 1002, 1, 1)


# 切换播放状态
def switch_play_status():
    time.sleep(1)
    m.click(800, 500, 1, 1)


# 切换录屏状态 F9
def switch_record_status():
    k.press_key(k.function_keys[9])
    k.release_key(k.function_keys[9])


def goto_url(url):
    m.click(700, 80)
    k.press_keys([k.control_key, 'a'])
    time.sleep(1)
    # 输入url
    k.type_string(url)
    # 回车
    k.press_key(k.enter_key)
    time.sleep(1)
    k.press_key(k.enter_key)
    time.sleep(1)


# 截图，获取播放按钮的状态
def screenshots():
    same_tames = 0
    global playing, start_time, is_test, running
    while running:
        img = ImageGrab.grab()
        img = img.convert('L')
        img.save('older.jpg')
        time.sleep(5)
        img = ImageGrab.grab()
        img = img.convert('L')
        img.save('new.jpg')
        if calculate("older.jpg", "older.jpg") == 1:
            same_tames += 1
        else:
            same_tames = 0

        # 截图
        if same_tames < 10:
            playing = True
            # 到了10 分钟就跳到最后，测试使用
            if is_test and time.time() - start_time > 60 * 5:
                un_full_screen()
                playing = False
            else:
                pass
        else:
            if time.time() - start_time < 60 * 5:
                # 如果开始播放时是停止状态
                playing = True
                switch_play_status()
            else:
                # 如果播放结束
                un_full_screen()
                playing = False


# 计算单通道的直方图的相似值
# 1.0 表示相似度最好
def calculate(image1_path, image2_path):
    imageA = cv2.imread(image1_path)
    imageB = cv2.imread(image2_path)
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    return score


def main():
    global start_time, playing, running
    # 打开浏览器
    webbrowser.open("www.baidu.com")
    t1 = threading.Thread(target=screenshots)
    t1.start()
    for url in courseUrlList:
        start_time = time.time()
        print(url)
        # 跳转到视频页面
        time.sleep(5)
        goto_url(url)
        # 全屏
        time.sleep(5)
        full_screen()
        # 进度条到最开始位置
        to_start()
        while playing:
            pass
        print("END-->" + url)
    # 结束
    while (not playing) and (time.time() - start_time > 20):
        running = False
        switch_record_status()
        time.sleep(1)
        switch_record_status()
        sys.exit(0)


# 测试代码
# 获取浏览器地址输入栏的坐标 700 ，80
# 屏幕中间位置 800 500
# 进度条的开始位置 0,1002 结束位置：1916,1002
def getM_xy():
    try:
        while True:
            x, y = pag.position()
            pos = "Position:" + str(x).rjust(4) + ',' + str(y).rjust(4)
            print(pos)
            time.sleep(10)
    except KeyboardInterrupt:
        print('end....')


# 二值化图片
def convert_image():
    img = Image.open('blank.jpg')
    img = img.convert('L')
    img.save('blank_L.jpg')

# main()
# getM_xy()
# convert_image()
