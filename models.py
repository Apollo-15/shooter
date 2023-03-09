from pygame import *
from random import randint
from time import time as t

WINDOW_SIZE = (700, 500)
SPRITE_SIZE = (90, 50)
DOWN = 1
LEFT = 2

FPS = 30
timer = t()

window = display.set_mode(WINDOW_SIZE)

bullets = sprite.Group()

WHITE = (255, 255, 255)

font.init()
font_counter = font.SysFont('Comic Sans MS', 25, True)
font_message = font.SysFont('Times New Roman', 70, True)

win = font_message.render('WIN!', 1, WHITE)
lose = font_message.render('Lose!', 1, WHITE)   


class Score():
    def __init__(self):
        self.lost_enemy = 0
        self.kill_enemy = 0
    def show(self):
        self.lost_enemy_label = font_counter.render("Пропущено: " + str(self.lost_enemy), 1, WHITE)
        self.kill_enemy_label = font_counter.render("Знищено: " + str(self.kill_enemy), 1, WHITE)
        window.blit(self.lost_enemy_label, (0, 0))
        window.blit(self.kill_enemy_label, (0, 35))

counter = Score()

class GameSprite(sprite.Sprite):
    def __init__(self, image_name, x_pos, y_pos, speed, size):
        super().__init__()
        self.image = transform.scale(image.load(image_name), size)
        self.speed = speed
        self.size = 70.50
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y <= 0:
            self.kill()

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()

        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < WINDOW_SIZE[1] - SPRITE_SIZE[1]:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < WINDOW_SIZE[0] - SPRITE_SIZE[0]:
            self.rect.x += self.speed

    def fire(self):
        keys = key.get_pressed()
        global timer
        if t() - timer > 0.5:
            charge_label = font_counter.render('Заряджено...', 1, WHITE)
            if keys [K_SPACE]:
                fire = mixer.Sound('fire.ogg')
                fire.play()
                bullets.add(Bullet("bullet.png", self.rect.x - 11, self.rect.y + 18, 3, (50, 100)))

                timer = t()
            
            else:
                charge_label = font_counter.render('Перезарядка...', 1, WHITE)

class Enemy(GameSprite):
    def __init__(self, image_name, x_pos, y_pos, speed, direction, size):
        super().__init__(image_name, x_pos, y_pos, speed, size)
        self.direction = direction

    def update(self):
        if self.direction == DOWN:
            global lost_enemy
            if self.rect.y < WINDOW_SIZE[1]:
                self.rect.y += self.speed
            else: 
                self.rect.y = 0
                self.rect.x = randint(0, WINDOW_SIZE[0] - SPRITE_SIZE[0])
                self.speed = randint(3, 5)
                lost_enemy += 1
        elif self.direction == LEFT:
            if self.rect.x > 0:
                self.rect.x -= self.speed
            elif self.rect.x < WINDOW_SIZE[0]:
                self.rect.x += self.speed



    def update(self):
        if self.rect.y < WINDOW_SIZE[1]:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(0, WINDOW_SIZE[0] - SPRITE_SIZE[0])
            self.speed = randint(3, 5)
            counter.lost_enemy += 1