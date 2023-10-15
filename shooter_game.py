from typing import Any
from pygame import *
from random import randint


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.Font(None, 36)
font = font.Font(None,50)


img_back = "galaxy.jpg" 
img_hero = "rocket.png" 
img_enemy = "ufo.png" 

score = 0 
lost = 0
lost_max = 3

win = font.render('Вы выйграли!',True,(255,215,0))
lose = font.render('Вы проиграли!',True,(180,0,0))


class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        
        sprite.Sprite.__init__(self)

       
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

      
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullets('bullet.png',self.rect.x+40 ,self.rect.y,15,20,15)
        bullets_1.add(bullet)

  
class Enemy(GameSprite):
   
    def update(self):
        self.rect.y += self.speed
        global lost
       
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullets(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))


ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets_1 = sprite.Group()

finish = False

run = True 
while run:
   
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()

    if not finish:
      
        window.blit(background,(0,0))

 
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
            
        ship.update()
        monsters.update()

        
        ship.reset()
        monsters.draw(window)

        bullets_1.draw(window)
        bullets_1.update()

        collison = sprite.groupcollide(monsters,bullets_1,True,True)

        for h in collison:
            score+=1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship,monsters,False) or lost >= 3:
            finish = True
            window.blit(lose,(230,150))
            
        if score >= 15:
            finish = True
            window.blit(win,(230,150))

        display.update()
    
        time.delay(50)