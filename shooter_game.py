from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

img_hero = "rocket.png"
img_back = "galaxy.jpg"
img_enemy = "ufo.png"
img_asteroid = "asteroid.png"

score = 0 
lost = 0
max_lost = 3
goal = 5
life = 3
reload_time = False
num_fire = 0


font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render("You win", True, (50,0,100))
lose = font1.render("You lose", True, (200, 10,20))
font2 = font.SysFont("Arial", 36)


class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x, size_y, player_speed ):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect  = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

img_bullet = "bullet.png"
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))

background = transform.scale(image.load(img_back), (win_width,win_height))


ship = Player(img_hero, 5, 400, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(1,6):
    monster = Enemy(img_enemy, randint(90, 620), -40, 80, 50, randint(1,5))
    monsters.add(monster)

for i in range(1,3):
    asteroid = Enemy(img_asteroid, randint(30,670), -40, 80, 50, randint(1,7) )
    asteroids.add(asteroid)
finish = False
run = True
while run:     
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and not finish:
            if e.key == K_SPACE:
                if num_fire < 5 and reload_time == False:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()
                if num_fire >= 5 and reload_time == False:
                    last_time = timer()
                    reload_time = True
    if not finish:
        window.blit(background, (0,0))
        ship.update()
        bullets.update()
        monsters.update()
        asteroids.update()
        ship.reset()    
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        if reload_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("wait, reload", True, (150,20,20))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                reload_time = False
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(90, 620), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters, False) or sprite.spritecollide(ship, asteroids, False) or lost >= max_lost:
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        if score >= goal:
            window.blit(win, (200, 200))
            finish = True
        text_score = font2.render("Рахунок: "+str(score), True, (255, 230,40))
        window.blit(text_score, (20,10))
        text_life = font2.render('Life: '+str(life), True, (255, 255, 255))
        window.blit(text_life, (590, 10))

        display.update()
    else:
        pass #перезапуск гри 
    
    time.delay(60) 