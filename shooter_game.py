from random import randint
from pygame import *
from time import time as timer
window=display.set_mode((1000,700))
display.set_caption('piu_piu')
fon=transform.scale(image.load('galaxy.jpg'),(1000,700))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
piu=mixer.Sound('fire.ogg')
font.init()
font=font.SysFont('Arial',35)
score=0
miss=0
class zxc(sprite.Sprite):
    def __init__(self, pi_image, pi_x, pi_y, size_x, size_y, pi_step):
        super().__init__()
        self.image=transform.scale(image.load(pi_image),(size_x,size_y))
        self.rect=self.image.get_rect()
        self.rect.x=pi_x
        self.rect.y=pi_y
        self.step=pi_step
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Hero(zxc):
    def control(self):
        knopochki=key.get_pressed()
        if knopochki[K_a] and self.rect.x>0:
            self.rect.x-=self.step
        if knopochki[K_d] and self.rect.x<920:
            self.rect.x+=self.step
    def fire(self):
        bullet=Bullet('bullet.png',self.rect.x+30,self.rect.y,20,20,15)
        bullets.add(bullet)
class Enemy(zxc):
    def update(self):
        self.rect.y+=self.step
        if self.rect.y>700:
            self.rect.y=0
            self.rect.x=randint(0,920)
class Enemy_1(zxc):
    def update(self):
        self.rect.y+=self.step
        global miss
        if self.rect.y>700:
            miss+=1
            self.rect.y=0
            self.rect.x=randint(0,920)
class Bullet(zxc):
    def update(self):
        self.rect.y-=self.step
        if self.rect.y<0:
            self.kill()
game=True
finish=False
clock=time.Clock()
Kolya=Hero('rocket.png',460,600,80,100,10)
ufos=sprite.Group()
bullets=sprite.Group()
asteroids=sprite.Group()
for i in range(1,3):
    asteroid=Enemy_1('asteroid.png',randint(80,920),0,80,80,randint(1,3))
    asteroids.add(asteroid)
for i in range(1,5):
    ufo=Enemy('ufo.png',randint(0,920),0,80,80,randint(1,5))
    ufos.add(ufo)
kol_bullets=0
r=False
while game:
    for e in event.get():
        if e.type==QUIT:
            game=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                if kol_bullets<5 and r==False:
                    kol_bullets+=1
                    piu.play()
                    Kolya.fire()
                if kol_bullets>= 5 and r==False:
                    start_t=timer()
                    r=True
    if finish!=True:
        window.blit(fon,(0,0))
        score_text=font.render('Счёт: '+str(score),True,(25,45,195))
        miss_text=font.render('Пропущено: '+str(miss),True,(250,5,17))
        window.blit(score_text,(10,10))
        window.blit(miss_text,(10,35))
        Kolya.reset()
        Kolya.control()
        ufos.update()
        ufos.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        if r==True:
            end_t=timer()
            if end_t-start_t<2:
                text_r=font.render('Перезарядка',True,(255,255,53))
                window.blit(text_r,(500,350))
            else:  
                r=False
                kol_bullets=0
        if sprite.spritecollide(Kolya,ufos,False)or sprite.spritecollide(Kolya,asteroids,False)or miss>=5:
            finish=True
            text_lose=font.render('Вы проиграли',True,(250,36,53))
            window.blit(text_lose,(500,350))
        babah=sprite.groupcollide(bullets,ufos,True,True)
        for i in babah:
            score+=1
            ufo=Enemy('ufo.png',randint(80,920),0,80,80,randint(1,5))
            ufos.add(ufo)
        if score>=50:
            finish=True
            text_win=font.render('Вы выиграли',True,(250,36,53))
            window.blit(text_lose,(500,350))
        display.update()
    clock.tick(60)