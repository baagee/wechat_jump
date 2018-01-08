# coding=utf-8

import os
from PIL import Image, ImageDraw, ImageFont
import pygame
from pygame.locals import *
import time
import math
import cv2
import numpy as np
import datetime


class WeChatJump(object):
    pos_1 = pos_2 = pos_3 = pos_4 = 0

    def __init__(self):
        if not os.path.exists('./pictures'):
            os.mkdir('./pictures')
        self.font = ImageFont.truetype("./EurostileLTStd.otf", 13)
        self.base_path = os.getcwd()
        self.screen = pygame.display.set_mode(self.__getScreen(), 0, 32)
        pygame.display.set_caption('微信跳一跳辅助')
        self.__getChessPosition()
        self.__flushGame("./1Thumb.png")

    def __getScreen(self):
        os.system('%s\\adb\\adb.exe shell screencap -p /sdcard/1.png' % self.base_path)
        os.system('%s\\adb\\adb.exe pull /sdcard/1.png' % self.base_path)
        image = Image.open('./1.png', 'r')
        image.thumbnail((394, 700))
        draw = ImageDraw.Draw(image)
        draw.rectangle([(330, 13), (375, 45)], fill='#aaaeb6')
        image.save("./1Thumb.png", format='png')
        return image.size

    def __markThumb(self, top_x, top_y):
        image = Image.open('./1Thumb.png')
        draw = ImageDraw.Draw(image)
        draw.line([top_x, top_y, self.pos_1, self.pos_2], fill=(0, 255, 0), width=2)
        draw.text((self.pos_1, self.pos_2), 'x=%s, y=%s' % (self.pos_1, self.pos_2), font=self.font, fill='#000000')
        image.save("./1Thumb.png", format='png')

    def __getChessPosition(self):
        img = cv2.imread('./1Thumb.png')
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            circles1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 600, param1=100, param2=25, minRadius=9,
                                        maxRadius=13)
            circles = np.uint16(np.around(circles1))
            circle = circles[0][0]
        except Exception as e:
            print('Error: %s' % e)
            exit()
        else:
            self.pos_1, self.pos_2 = circle[0], circle[1] + 59
            self.__markThumb(circle[0], circle[1])

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0] == 1:
                        self.pos_3, self.pos_4 = pygame.mouse.get_pos()
            if self.pos_1 != 0 and self.pos_2 != 0 and self.pos_3 != 0 and self.pos_4 != 0:
                press_time = int(
                        math.sqrt(abs(self.pos_1 - self.pos_3) ** 2 + abs(self.pos_2 - self.pos_4) ** 2) * 3.8)
                print('pos_1=%s, pos_2=%s, pos_3=%s, pos_4=%s, press_time=%s' % (
                    self.pos_1, self.pos_2, self.pos_3, self.pos_4, press_time))
                self.__addJumpLine(press_time)
                self.__flushGame("./pictures/%s.png" % self.nowTime)
                self.__jump(press_time)
                self.pos_1 = self.pos_2 = self.pos_3 = self.pos_4 = 0
                time.sleep(1)
                self.__getScreen()
                self.__getChessPosition()
                self.__flushGame('./1Thumb.png')

    def __addJumpLine(self, press_time):
        image = Image.open('./1Thumb.png')
        draw = ImageDraw.Draw(image)
        draw.line([self.pos_3, self.pos_4, self.pos_1, self.pos_2], fill=(255, 0, 0), width=2)
        draw.text((self.pos_3, self.pos_4), 'x=%s, y=%s' % (self.pos_3, self.pos_4), font=self.font, fill='#000000')
        draw.text((130, 160), 'pressTime=%s ms' % (press_time), font=self.font, fill='#000000')
        self.nowTime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        image.save("./pictures/%s.png" % self.nowTime, format='png')

    def __jump(self, press_time):
        cmd = '%s\\adb\\adb.exe shell input swipe 600 700 600 700 %s' % (self.base_path, press_time)
        os.system(cmd)

    def __flushGame(self, image):
        background = pygame.image.load(image).convert()
        self.screen.blit(background, (0, 0))
        pygame.display.update()


wj = WeChatJump()
wj.run()
