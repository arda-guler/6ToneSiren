import pyautogui
import pygame
import time
import random
import ctypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import os

pygame.mixer.init()
os.system("cls")
sound = pygame.mixer.Sound('sixtone.wav')
sound_playing = False

def play_sound_loop():
    sound.play(loops=-1)

def stop_sound():
    sound.stop()

def set_volume(volume_level):
    devices = ctypes.windll.winmm.waveOutGetNumDevs()
    for i in range(devices):
        vol = int(volume_level * 0xFFFF / 100)
        ctypes.windll.winmm.waveOutSetVolume(i, vol | (vol << 16))

# this makes a big assumption and may not do the intended thing
def set_audio_device_to_builtin_speaker():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    # Get the default audio device and set its volume level
    volume.SetMasterVolumeLevelScalar(1.0, None)  # Set to full volume

def monitor_user_activity():
    global sound_playing
    
    last_mouse_position = pyautogui.position()
    last_activity_time = time.time()

    while True:
        time.sleep(1)
        
        current_mouse_position = pyautogui.position()
        
        if current_mouse_position != last_mouse_position:
            last_mouse_position = current_mouse_position
            last_activity_time = time.time()
            stop_sound()
        
        inactivity_time = time.time() - last_activity_time
        
        if inactivity_time >= 600:  # 10 minutes
            # Set a random waiting time between 2 and 5 minutes
            random_wait_time = random.uniform(120, 300)
            
            time.sleep(random_wait_time)
            
            if pyautogui.position() == last_mouse_position and not sound_playing:
                set_volume(100)
                set_audio_device_to_builtin_speaker()
                play_sound_loop()
                sound_playing = True
            elif pyautogui.position() != last_mouse_position:
                last_mouse_position = pyautogui.position()
                last_activity_time = time.time()
                stop_sound()
                sound_playing = False

if __name__ == "__main__":
    monitor_user_activity()
