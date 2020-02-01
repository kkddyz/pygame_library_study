import os,sys
#  These allow us to do things like create platform independent file paths.
import pygame
#   This module contains a subset of pygame. The members of this module are
#   commonly used  constants and functions that  have proven useful to put into
#   your program's global namespace.


from pygame.locals import *
def main():
    # Some pygame modules are optional, and if they aren't found, their value is set to None.
    if not pygame.font :print("Waring,fonts disabled")
    if not pygame.mixer :print("Waring,sound disabled")

    """
    Here we have two functions we can use to load images and sounds.
    We will look at each function individually in this section.
    """


    # Loading Resource 通过os来解决导入外部文件的问题

def load_image(name,colorkey=None): # 参数的用途是什么？？
    # name要load的图片名 colorkey是可选参数

    fullname = os.path.join("resource file",name)
    #In this example all the resources are in a "resource file " subdirectory
    # The first thing this function does is create a full pathname to the file
    #pathname will be created that works for whatever platform the game is running on.
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message : ## message 作为 pygame.error 的一个 instance
        print('Cannot load image:', name)
        # 逗号是啥意思print("aaa","bbb") --> aaa bbb 逗号是分隔符，输出后带空格
        raise SystemExit(message) #也就是不会执行后面的代码
        """ 通过 raise ，exit gracefully"""
        # SystemExit（）解释器请求退出异常 用给定的状态和消息创建一个新的异常。
        # 状态为true，false或整数。如果没有给出状态，则使用true
    image = image.convert()
    # colorkey 用于 将图像的颜色边框设置为透明
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
if __name__ == "__main__":
    main()