import time
from math import ceil
# from pygame._sdl2 import get_num_audio_devices, get_audio_device_name
from pygame import mixer
from mutagen.mp3 import MP3
mixer.init()
# print([get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))])
file_name = '你看那风有吹-小青.mp3'
mixer.quit()
mixer.init(devicename='Line 1 (Virtual Audio Cable)')
mixer.music.load('你看那风有吹-小青.mp3')
mixer.music.play()
audio = MP3(file_name)
time.sleep(ceil(audio.info.length) + 0.3)
# 設置音量
mixer.music.set_volume(0.5)

mixer.music.stop()