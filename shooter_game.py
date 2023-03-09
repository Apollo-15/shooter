from models import *
from random import randint

display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), WINDOW_SIZE)


player = Player("rocket.png", WINDOW_SIZE[0] / 2 - SPRITE_SIZE[0] / 2, WINDOW_SIZE[1] - SPRITE_SIZE[1], 5, (50, 50))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play(-1)


clock = time.Clock()
finish = False
game = True

asteroids = sprite.Group()
enemies = sprite.Group()
for i in range(3):
    enemies.add(Enemy("ufo.png", randint(0, WINDOW_SIZE[0] - SPRITE_SIZE[0]), 0, 3, DOWN, (90, 70)))

for i in range(3):
    asteroids.add(Enemy("asteroid.png", randint(WINDOW_SIZE[0], WINDOW_SIZE[0] + 100), randint(0, WINDOW_SIZE[1] - SPRITE_SIZE[1] * 2 - 20), 3, LEFT, (90, 70)))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))
    
        for enemy in enemies:
            for bullet in bullets:
                if sprite.collide_rect(enemy, bullet):
                    enemy.rect.y = 0
                    enemy.rect.x = randint(0, WINDOW_SIZE[0] - SPRITE_SIZE[0])
                    enemy.kill()
                    bullet.kill()
                    counter.kill_enemy += 1

                    enemies.add(Enemy("ufo.png", randint(0, WINDOW_SIZE[0] - SPRITE_SIZE[0]), randint(-100, 0), randint(3, 5), DOWN, (90, 70)))


        player.move()
        player.reset()
        player.fire()


        asteroids.draw(window)
        asteroids.update()
        enemies.draw(window)
        enemies.update()

        bullets.update()
        bullets.draw(window)

        counter.show()
        sprite.groupcollide(bullets, asteroids, True, False)
        if counter.kill_enemy >= 30:
            finish = True
            window.blit(win, (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2))
        elif counter.lost_enemy >= 50 or sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(lose, (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2))

        display.update()
        clock.tick(FPS)