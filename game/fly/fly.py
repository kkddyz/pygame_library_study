import sys,pygame
from pygame.locals import * #引入常量和一些函数

import random

# 内置事件 和 对象的 动作 有什么不一样
# 内置时事件对应一串连续的整数常量，其中最大的就是USEREVENT
#自定义事件
ADDENEMY = pygame.USEREVENT + 1 # 事件名
pygame.time.set_timer(ADDENEMY,150) # 每250毫秒生成一个事件


#玩家 是个什么东西？？？ 精灵我理解就是会动的图像
class Player(pygame.sprite.Sprite): #这是个什么类？ Sprite精灵
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        # 表示 图像 用image代替surface
        # self.surf = pygame.Surface((75,25)) # 尺寸是个元组 被只当作一个参数
        # self.surf.fill(Aquamarine4) # 里面他妈的有括号是个整体，也就是说，有其他 args fill(self,color,rect,special_flag)
        self.image = pygame.image.load("jet.jpg").convert()
        self.image.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.image.get_rect() #rect是成员变量 不是局部变量
        self.player_speed = 2

    #这里 key[K_UP]如何理解？？
    #update函数必须在主循环里被调用 再能实现
    def update(self, key):

        if key[K_UP]:
            # move_ip 作何解？？ a.rect.move(2,0) 会创建一个新的rect对象
            #a.rect.move_ip(2,0) == a.rect=a.rect.move_ip(2,0)
            # in_place 常规方法是 返回move后的对象，原来的图像不会清除，
            # 用这个就是常规意义上的移动
            self.rect.move_ip(0,-self.player_speed)
        if key[K_DOWN]:
            self.rect.move_ip(0,self.player_speed)
        if key[K_LEFT]:
            self.rect.move_ip(-self.player_speed,0)
        if key[K_RIGHT]:
            self.rect.move_ip(self.player_speed,0)

        # 限定player在屏幕里
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 1400 :
            self.rect.right = 1400
        elif self.rect.top < 0:
            self.rect.top = 0
            # 这里的bottom改成bot也可以，为什么？
        elif self.rect.bottom >700:
            self.rect.bottom = 700
# 敌人 不在屏幕范围内的surface依然存在，只是invisible而已。
class Enemy (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.surf = pygame.Surface((25,11))
        # self.surf.fill(LemonChiffon)
        self.image = pygame.image.load("missile.jpg").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        # self.image.set_colorkey((255,255,255),RLEACCEL)# 这个后面的flags参数干 加快blit 的速度
        #？？ 为什么飞机可以透明，子弹不起作用
        # 把敌人的位置设置在看不见的地方
        self.rect = self.image.get_rect(center=(1420,random.randint(0,600))) # 可以在 get_rect方法设置初始位置
        self.speed = random.randint(2,5) #randint[a,b) 左闭右开

    def update(self): # 敌人自右向左移动 上下不移动
        self.rect.move_ip(-self.speed,0)
                    # 消除出界的敌人 Sprite的内建方法
        if self.rect.right < 0:
            self.kill()
# update不是事件
def main():
    count = 0
    num = 0
    lives = 10
    # 1. 初始化所有引入的模块
    pygame.init()

    # 2.设置display（屏幕）对象 screen <-- display
    screen = pygame.display.set_mode((1400, 700))  # 尺寸 不可拉伸
    background = pygame.image.load("background.jpg").convert()
    # 3.1 初始化玩家精灵对象的surf
    player = Player()

    #设置两个精灵组 一个包括所有敌人 一个包括敌人和玩家
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # 窗口主循环
    while True:
        # 遍历事件队列 按时间触发的事件排成队列 #系统事件#
        for event in pygame.event.get():
            if event.type == QUIT:  # 显然QUIT
                pygame.quit()
                sys.exit()  # 这两个离开有啥区别
            elif event.type == KEYDOWN: #KEYDOWN是按下键盘 对应KEYUP 弹起键盘
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        # 不论是否有事件发生 ，都会不断刷新

        # 更新屏幕 background
        screen.blit(background,(0,0))

        # 更新屏幕内容 surface ***************************

        # 获得按键 假如没有 返回 None if key==none不会调用函数
        key = pygame.key.get_pressed()

        # 更新，放置玩家
        player.update(key)
        screen.blit(player.image, player.rect)


        # 更新,放置敌人
        for enemy in enemies:
            enemy.update()
            screen.blit(enemy.image, enemy.rect)

        # 碰撞检测（灵魂所在）# 如果位置重复
        if pygame.sprite.spritecollide(player, enemies,True):
            # 由于碰撞后销毁 所以只会数到一次重叠

            num = num + 1
            lives = lives -1
            print("发生%d次碰撞"%(num))
            print("你还有%d条命"%(lives))

        #*************************************************
        # 更新界面 这里发生了什么？？
        pygame.display.flip() #更新整个带显示对象到screen上

if __name__=="__main__":
    main()



