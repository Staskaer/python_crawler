
# -*- coding: utf-8 -*-
# 由于模拟拖动轨迹的计算和滑动的算法可能有问题，目前的成功率只有10%左右
# 可能需要优化的地方为
# 滑动函数（动作链执行速度过慢效率低下）
# 轨迹计算函数（计算出的轨迹不宜绕过轨迹验证，与计算公式有关）


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import random

from PIL import Image

web = 'http://literallycanvas.com/'


def init():
    # 定义为全局变量，方便其他模块使用
    global url, browser, username, password, wait
    url = 'https://passport.bilibili.com/login'
    browser = webdriver.Chrome()
    username = '***********'
    password = '***********'
    wait = WebDriverWait(browser, 20)


def login():
    # 登录的操作
    browser.get(url)
    user = wait.until(EC.presence_of_element_located(
        (By.ID, 'login-username')))
    passwd = wait.until(
        EC.presence_of_element_located((By.ID, 'login-passwd')))
    user.send_keys(username)
    passwd.send_keys(password)

    # 获取登录按钮
    login_btn = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'a.btn.btn-login')))
    # 随机延时点击
    time.sleep(random.random() * 3)
    login_btn.click()

# 设置元素可见


def show_element(element):
    browser.execute_script(
        "arguments[0].style=arguments[1]", element, "display: block;")

# 设置元素不可见


def hide_element(element):
    browser.execute_script(
        "arguments[0].style=arguments[1]", element, "display: none;")

# 截图


def save_pic(obj, name):
    try:
        pic_url = browser.save_screenshot('.\\bilibili.png')
        print("%s:截图成功!" % pic_url)

        # 获取元素位置信息
        left = obj.location['x']
        top = obj.location['y']
        right = left + obj.size['width']
        bottom = top + obj.size['height']

        print('图：'+name)
        print('Left %s' % left)
        print('Top %s' % top)
        print('Right %s' % right)
        print('Bottom %s' % bottom)
        print('')

        im = Image.open('.\\bilibili.png')
        im = im.crop((left*1.23, top*1.23, right*1.23,
                      bottom*1.23))  # 元素裁剪，其中的乘数取决于分辨率
        file_name = 'bili_'+name+'.png'
        im.save(file_name)  # 元素截图
    except BaseException as msg:
        print("%s:截图失败!" % msg)


def cut():
    # 具体的裁剪操作
    time.sleep(1)
    c_background = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'canvas.geetest_canvas_bg.geetest_absolute')))
    c_slice = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'canvas.geetest_canvas_slice.geetest_absolute')))
    c_full_bg = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'canvas.geetest_canvas_fullbg.geetest_fade.geetest_absolute')))
    hide_element(c_slice)
    save_pic(c_background, 'back')
    show_element(c_slice)
    save_pic(c_slice, 'slice')
    show_element(c_full_bg)
    save_pic(c_full_bg, 'full')

# 判断像素是否相同


def is_pixel_equal(bg_image, fullbg_image, x, y):
    """
    :param bg_image: (Image)缺口图片
    :param fullbg_image: (Image)完整图片
    :param x: (Int)位置x
    :param y: (Int)位置y
    :return: (Boolean)像素是否相同
    """

    # 获取缺口图片的像素点(按照RGB格式)
    bg_pixel = bg_image.load()[x, y]
    # 获取完整图片的像素点(按照RGB格式)
    fullbg_pixel = fullbg_image.load()[x, y]
    # 设置一个判定值，像素值之差超过判定值则认为该像素不相同
    threshold = 60
    # 判断像素的各个颜色之差，abs()用于取绝对值
    if (abs(bg_pixel[0] - fullbg_pixel[0] < threshold) and abs(bg_pixel[1] - fullbg_pixel[1] < threshold) and abs(bg_pixel[2] - fullbg_pixel[2] < threshold)):
        # 如果差值在判断值之内，返回是相同像素
        return True
    else:
        return False


# 计算滑块移动距离
def get_distance(bg_image, fullbg_image):
    '''
    :param bg_image: (Image)缺口图片
    :param fullbg_image: (Image)完整图片
    :return: (Int)缺口离滑块的距离
    '''
    # 滑块的初始位置
    distance = 21
    # 遍历像素点横纵坐标
    for i in range(distance, fullbg_image.size[0]):
        for j in range(fullbg_image.size[1]):
            if not is_pixel_equal(fullbg_image, bg_image, i, j):
                k = i-9  # -9是把初始滑块距离最左侧的像素点考虑进去，如果截取的时候左侧刚好卡在截线上，则去掉此差值运算
                return k


# 构造滑动轨迹
def get_trace(distance):
    # 这个函数需要大规模的修改
    # 主要是轨迹构造方程上的取值
    # 包含但不仅限于加速和减速阶段的a的大小
    # 以及加速和减速阶段的区分
    # （因为模拟拖动函数的动作链似乎无法加速执行，只能通过巧妙的构造轨迹来加速执行效率和成功率）
    # 在改变轨迹构造函数的同时还需要兼顾距离修正系数！
    # 以下是记录有效的数据组[（a,-a,轨迹划分系数,距离修正系数）:成功率]
    # （5,-9,2/3,0.92||0.93）:10%
    '''
    :param distance: (Int)缺口离滑块的距离
    :return: (List)移动轨迹
    '''
    track = []
    current = 0
    mid = distance*2/3  # 分成加速和减速两段轨迹
    t = 0.2
    v = 0
    while current < distance:
        if current < mid:
            a = 5
        else:
            a = -9
        v0 = v
        v = v0+a*t
        move = v0*t + 1/2*a*t*t
        current += move
        track.append(round(move, 2))
    return track


def move_to_gap(trace):  # 模拟拖动
    # 得到滑块标签
    #slider = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_slider_knob')))
    slider = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div.geetest_slider_button')))
    # 使用click_and_hold()方法悬停在滑块上，perform()方法用于执行
    ActionChains(browser).click_and_hold(slider).perform()
    for x in trace:
        # 使用move_by_offset()方法拖动滑块，perform()方法用于执行
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
    # 小范围震荡
    ActionChains(browser).move_by_offset(xoffset=3, yoffset=0).perform()
    ActionChains(browser).move_by_offset(xoffset=-3, yoffset=0).perform()
    ActionChains(browser).move_by_offset(xoffset=-2, yoffset=0).perform()
    ActionChains(browser).move_by_offset(xoffset=2, yoffset=0).perform()
    # 模拟人类对准时间
    time.sleep(0.5)
    # 释放滑块
    ActionChains(browser).release().perform()


def slide():
    distance = get_distance(Image.open('.\\bili_back.png'),
                            Image.open('.\\bili_full.png'))
    print('计算偏移量为：%s Px' % distance)
    # 计算移动轨迹
    trace = get_trace(distance*0.92)  # 这个参数取决于系统配置，需要修改来获得最佳的适配
    # 移动滑块
    move_to_gap(trace)
    time.sleep(4)
    browser.quit()


init()
login()
cut()
slide()
