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
need_show = False
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
    show_progress_bar_same_time()


# 切换播放状态
def switch_play_status():
    time.sleep(1)
    m.click(800, 500, 1, 1)


# 切换录屏状态 F9
def switch_record_status():
    k.press_key(k.function_keys[9])
    k.release_key(k.function_keys[9])


def goto_url(url):
    # 等待浏览器完全打开
    while need_show:
        # 等待鼠标不吸附在控制条
        time.sleep(1)
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


# 显示进度条,控制条
def show_progress_bar():
    global playing, need_show, start_time, is_test, running
    while running:
        if need_show:
            time.sleep(0.5)
            m.move(1910, 1002)
            screenshots()
            m.move(1910, 1000)
        else:
            time.sleep(1)


# 在to_start 调用后 显示进度条,控制条5秒
def show_progress_bar_same_time():
    for i in range(10):
        m.move(1910, 1002)
        time.sleep(0.5)
        m.move(1910, 1000)


# 截图，获取播放按钮的状态
def screenshots():
    global playing, need_show, start_time, is_test, running
    old_x, old_y = 20, 1020
    new_x, new_y = 60, 1060
    img = ImageGrab.grab((old_x, old_y, new_x, new_y))
    img = img.convert('L')
    img.save('status.jpg')
    # 非全屏状态下的截图
    if calculate("status.jpg", "playing_L.jpg") < 0.5 and calculate("status.jpg", "stopped_L.jpg") < 0.5:
        playing = False
        need_show = False
        if is_test and time.time() - start_time < 30:
            full_screen()
        return

    # 全屏状态下的截图
    if calculate("status.jpg", "playing_L.jpg") > calculate("status.jpg", "stopped_L.jpg"):
        playing = True
        # 到了10 分钟就跳到最后，测试使用
        if is_test and time.time() - start_time > 40:
            un_full_screen()
            playing = False
            need_show = False
        else:
            pass
    else:
        if time.time() - start_time < 20:
            # 如果开始播放时是停止状态
            playing = True
            need_show = True
            switch_play_status()
        else:
            # 如果播放结束
            un_full_screen()
            playing = False
            need_show = False


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
    global need_show, start_time, playing, running
    # 打开浏览器
    webbrowser.open("www.baidu.com")
    t1 = threading.Thread(target=show_progress_bar)
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
        # 显示进度条
        need_show = True
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
