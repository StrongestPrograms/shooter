from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.SysFont('Arial', 23)
font2 = font.SysFont('Arial', 35)
win = font2.render('YOU WIN', True, (0, 255, 0))
lose = font2.render('YOU LOSE', True, (255, 0, 0))

lost = 0
score = 0
life = 3

class GameSprite(sprite. Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 700:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('123.png', self.rect.right, self.rect.centery, 15, 20, randint(1, 3))
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.x = 700
            self.rect.y = randint(80, 420)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.x += randint(1,3)
        if self.rect.x > 700:
            self.kill()

win_width = 700
win_height = 500
ship = Player('1.png', 5, win_height-100, 80, 100, 7)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', 720, randint(80, 420), 80, 50, randint(1,5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', 720, randint(80, 420), 80, 50, randint(1,5))
    asteroids.add(asteroid)


mw = display.set_mode((700, 500))
display.set_caption('shooter')
bg = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
mixer.music.set_volume(0.1)
fire_sound.set_volume(0.1)

bullets = sprite.Group()
finish = False
run = True
num_fire = 0
rel_time = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time != True:
                    ship.fire()
                    fire_sound.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        mw.blit(bg, (0,0))

        text = font2.render(f'Счёт: {score}', True, (255, 255, 255))
        mw.blit(text,(10, 20))
        text_lose = font2.render(f'Пропущено: {lost}', True, (255, 255, 255))
        mw.blit(text_lose, (10, 50))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', 720, randint(80, 420), 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, True):
            finish = True
            mw.blit(lose,(200, 200))

        if rel_time:
            now_time = timer()
            if now_time - last_time <3:
                reload = font2.render('reload', True, (150, 0, 0))
                mw.blit(reload, (200, 400))
            else:
                num_fire = 0
                rel_time = False



        ship.reset()
        ship.update()
        monsters.draw(mw)
        monsters.update()
        bullets.draw(mw)
        bullets.update()
        asteroids.draw(mw)
        asteroids.update()
    display.update()
    time.delay(20)