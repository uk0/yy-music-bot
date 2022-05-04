# 对后台窗口截图
import time

import win32gui, win32ui, win32con
from ctypes import windll
from PIL import Image
import cv2
import numpy
import time
from math import ceil
# from pygame._sdl2 import get_num_audio_devices, get_audio_device_name
from pygame import mixer
from mutagen.mp3 import MP3

from wycloud import search

mixer.init()
mixer.quit()
mixer.init(devicename='Line 1 (Virtual Audio Cable)')

is_play = 0

user_list = ["2845564011", "6723594"]


def download(url, filename):
    from tqdm import tqdm
    import requests
    url = url.replace("\"", "")
    print(url.replace("\"", ""))
    response = requests.get(url, stream=True)
    with open(filename, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)


def get_all_windows():
    hWnd_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWnd_list)
    print(hWnd_list)
    yymain = win32gui.FindWindow("YYChannelWindow", None)
    return hWnd_list


def get_son_windows(parent):
    hWnd_child_list = []
    win32gui.EnumChildWindows(parent, lambda hWnd, param: param.append(hWnd), hWnd_child_list)
    print(hWnd_child_list)
    return hWnd_child_list


def get_title(hwnd):
    title = win32gui.GetWindowText(hwnd)
    # print('窗口标题:%s' % (title))
    return title


def get_clasname(hwnd):
    clasname = win32gui.GetClassName(hwnd)
    print('窗口类名:%s' % (clasname))
    return clasname


# 根据窗口名称获取句柄
def get_hwnd_from_name(name):
    hWnd_list = get_all_windows()
    for hwd in hWnd_list:
        title = get_title(hwd)
        if title == name:
            return hwd


def command(cmd: str):
    volume_cmd = cmd[0:1]
    volume = cmd[1:]
    sigin_cmd = cmd[0:1]
    amand = cmd[0:2]
    addsuper = cmd[0:8]
    user_ = cmd[8:]
    music_file_name = cmd[2:]
    global is_play
    if sigin_cmd == "5":
        if (is_play % 2) == 0:
            mixer.music.pause()
            print("pause")
            # mixer.music.stop()
        else:
            # mixer.music.stop()
            print("unpause")
            mixer.music.unpause()
        is_play = is_play + 1
        return
    if volume_cmd == "+":

        try:
            if type(eval(volume)) == int:
                mixer.music.set_volume(mixer.music.get_volume() + int(volume) * 0.01)
        except Exception as e:
            return
        return
    if volume_cmd == "-":
        try:
            if type(eval(volume)) == int:
                mixer.music.set_volume(mixer.music.get_volume() - int(volume) * 0.01)
        except Exception as e:
            return
        return
    # addsuper6723594
    if addsuper == "addsuper":
        user_list.append(user_)
        return
    if sigin_cmd == "4":
        print("上一曲")
        return
    if sigin_cmd == "6":
        print("下一曲")
        return
    if amand == "播放" or amand == "点歌":
        import os.path
        if music_file_name != "":
            filename, download_url = search(music_file_name)
            if os.path.isfile(filename + ".mp3"):
                t21 = threading.Thread(target=play_mp3, args=(filename + ".mp3",))
                print(filename + ".mp3", "找到了文件 直接播放")
                t21.start()
                t21.join()
                return
            else:
                if filename != "" and download_url != "null":
                    download(download_url, filename + ".mp3")
                    t1 = threading.Thread(target=play_mp3, args=(filename + ".mp3",))
                    print(filename + ".mp3", "没有找到文件 开始下载播放")
                    t1.start()
                    t1.join()
                    return


def play_mp3(file_name):
    # print([get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))])
    mixer.music.load(file_name)
    mixer.music.play()
    # audio = MP3(file_name)
    # time.sleep(ceil(audio.info.length) + 0.3)
    # # 設置音量
    # mixer.music.set_volume(0.2)
    # mixer.music.stop()


# 获取后台窗口的句柄，注意后台窗口不能最小化
hWnd = get_hwnd_from_name("280855-唐念")
# #获取句柄窗口的大小信息
left, top, right, bot = win32gui.GetWindowRect(hWnd)
width = right - left
height = bot - top
# 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
# hWndDC = win32gui.GetWindowDC(hWnd)  # 创建设备描述表
# mfcDC = win32ui.CreateDCFromHandle(hWndDC)  # 创建内存设备描述表
# saveDC = mfcDC.CreateCompatibleDC()  # 创建位图对象准备保存图片
# saveBitMap = win32ui.CreateBitmap()  # 为bitmap开辟存储空间
# saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)  # 将截图保存到saveBitMap中
# saveDC.SelectObject(saveBitMap)  # 保存bitmap到内存设备描述表
# saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)  # 如果要截图到打印设备：
# # ###最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1 #
# result = windll.user32.PrintWindow(hWnd, saveDC.GetSafeHdc(), 0)
# print(result)  # PrintWindow成功则输出1
# #保存图像
# ##方法一：windows api保存 ###保存bitmap到文件
# saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")
##方法二(第一部分)：PIL保存 ###获取位图信息
# bmpinfo = saveBitMap.GetInfo()
# bmpstr = saveBitMap.GetBitmapBits(True)  ###生成图像
# im_PIL = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
##方法二（后续转第二部分）
# ##方法三（第一部分）：
# opencv+numpy保存 ###获取位图信息
# signedIntsArray = saveBitMap.GetBitmapBits(True)

##方法三（后续转第二部分）
# #内存释放
# win32gui.DeleteObject(saveBitMap.GetHandle())
# saveDC.DeleteDC()
# mfcDC.DeleteDC()
# win32gui.ReleaseDC(hWnd, hWndDC)
##方法二（第二部分）：PIL保存 ###PrintWindow成功,保存到文件,显示到屏幕
# im_PIL.save("im_PIL.png")
# 保存
# im_PIL.show()  # 显示 ##方法三（第二部分）：opencv+numpy保存 ###PrintWindow成功，保存到文件，显示到屏幕
hWndDC = win32gui.GetWindowDC(hWnd)  # 创建设备描述表
mfcDC = win32ui.CreateDCFromHandle(hWndDC)  # 创建内存设备描述表
saveDC = mfcDC.CreateCompatibleDC()  # 创建位图对象准备保存图片
import threading
from paddleocr import PaddleOCR, draw_ocr

# Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
# 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
ocr = PaddleOCR(use_angle_cls=False, lang="ch")  # need to run only once to download and load model into memory
cache_map = dict()
while True:
    time.sleep(0.5)
    saveBitMap = win32ui.CreateBitmap()  # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)  # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)  # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)  # 如果要截图到打印设备：
    # ###最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1 #
    result = windll.user32.PrintWindow(hWnd, saveDC.GetSafeHdc(), 0)

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')
    im_opencv.shape = (height, width, 4)
    cropped = im_opencv[450:570, 265:600]
    cv2.cvtColor(cropped, cv2.COLOR_BGRA2RGB)
    cv2.imwrite("im_opencv.jpg", cropped, [int(cv2.THRESH_BINARY), 100])  # 保存
    # cv2.namedWindow('im_opencv')  # 命名窗口
    # cv2.imshow("im_opencv", im_opencv)  # 显示

    # key = cv2.waitKey(1) & 0xff
    # cv2.imshow('im_opencv', cropped)

    img_path = 'im_opencv.jpg'
    #
    next_line = False
    temp_str_att = ""
    result1 = ocr.ocr(img_path, cls=True)
    for line in result1:
        str_tm0p = line[1][0]
        str_tm0p = str_tm0p.replace("）", "####")
        str_tm0p = str_tm0p.replace("（", "####")
        import hashlib

        temp_str_att = str_tm0p + temp_str_att
        if len(str_tm0p.split("####")) == 3:
            if str_tm0p.split("####")[1] not in user_list:
                continue
            else:
                next_line = True
                # 第一步先找到  yyid然后去寻找下一行 command
                continue

        else:
            if next_line:
                # 这里是找到了 cmd
                if temp_str_att in cache_map.keys():
                    continue
                else:
                    cache_map[temp_str_att] = ""
                    next_line = False
                    print("command = ", str_tm0p)
                    command(str_tm0p)
        temp_str_att = ""
