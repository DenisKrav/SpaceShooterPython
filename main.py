from pygame import *
import sys
from random import randint
import os

def resource_path(relative_path):
    """Отримати абсолютний шлях до ресурсу, враховуючи запакований .exe"""
    try:
        # Якщо програма запакована у виконуваний файл
        base_path = sys._MEIPASS
    except AttributeError:
        # Якщо запускається як скрипт
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=(156, 37, 134)):
        self.rect = Rect(x, y, width, height)
        self.fill_color = color

    def change_color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        draw.rect(screen, self.fill_color, self.rect)

class Picture(Area):
    def __init__(self, fileName, x=0, y=0, width=10, height=10, isStar=False, color=(156, 37, 134)):
        Area.__init__(self, x, y, width, height, color)
        self.image = transform.scale(image.load(fileName), (width, height))
        self.isStar = isStar

    def draw_picture(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Label(Area):
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        super().__init__(x, y, width, height, color)

    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.text = text
        self.image = font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw_text(self, shift_x=0, shift_y=0):
        self.fill()
        screen.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

init()

sW = 700
sH = 700

backgroundImg = transform.scale(image.load(resource_path("assets/images/background.jpg")), (sW, sH))
screen = display.set_mode((sW, sH))

clock = time.Clock()

rocket = Picture(resource_path("assets/images/spaceship.png"), int(sW * 0.42), int(sH * 0.80), 60, 60)
rocketV = 10

ufos = []
ufoV = 2

bullets = []
bulletV = 15

finalLabel = Label(sW * 0.45, sH * 0.45, 100, 50, (0, 0, 0))
finalLabel2 = Label(sW * 0.1, sH * 0.5, 100, 50, (0, 0, 0))
finalLabel2.set_text("Press 'n' to start new game or 'q' to quit game.", 25, (255, 255, 255))
isWon = False

points = 0
scoreLabel = Label(50, 30, 0, 0, (0, 0, 0))
scoreLabel.set_text(f"Score: {points}", 30, (255, 255, 255))

shoot_sound = mixer.Sound(resource_path("assets/music/vyistrel2.mp3"))

fon_music = mixer.Sound(resource_path("assets/music/fonMusic.mp3"))
fon_music.play()

while True:
    if isWon:
        screen.fill((0, 0, 0))
        finalLabel.draw_text()
        finalLabel2.draw_text()

        keys = key.get_pressed()
        if keys[K_n]:
            bullets = []
            isWon = False
            for ufo in ufos:
                ufo.rect.x = randint(0, sW - ufo.rect.width)
                ufo.rect.y = randint(-200, -70)
                points = 0
                scoreLabel.set_text(f"Score: {points}", 30, (255, 255, 255))
        elif keys[K_q]:
            quit()
            sys.exit()
    else:

        if points == -20:
            isWon = True
            finalLabel.set_text("You loose!", 25, (255, 255, 255))

        screen.blit(backgroundImg, (0, 0))

        rocket.draw_picture()

        if randint(1, 100) < 2:
            ufo_x = randint(0, sW - 60)
            new_ufo = Picture(resource_path("assets/images/ufo2.png"), ufo_x, 0, 60, 60)
            isStar = randint(1, 100) < 10
            if isStar:
                new_ufo = Picture(resource_path("assets/images/star.png"), ufo_x, 0, 60, 60, True)
            ufos.append(new_ufo)

        ufos = [ufo for ufo in ufos if ufo.rect.y <= sH]

        for ufo in ufos:
            ufo.rect.y += ufoV
            if ufo.rect.y > sH:
                ufos.remove(ufo)
                points -= 1
                scoreLabel.set_text(f"Score: {points}", 30, (255, 255, 255))
            ufo.draw_picture()

        for bullet in bullets[:]:
            bullet.rect.y -= bulletV
            if bullet.rect.y < 0:
                bullets.remove(bullet)
            else:
                bullet.draw_picture()

        scoreLabel.draw_text()

        keys = key.get_pressed()
        if (keys[K_RIGHT] or keys[K_d]) and rocket.rect.x + rocket.rect.width < sW:
            rocket.rect.x += rocketV
        elif (keys[K_LEFT] or keys[K_a]) and rocket.rect.x > 0:
            rocket.rect.x -= rocketV

        for ufo in ufos:
            if rocket.rect.colliderect(ufo.rect):
                if ufo.isStar:
                    ufos.remove(ufo)
                    points += 5
                    scoreLabel.set_text(f"Score: {points}", 30, (255, 255, 255))
                else:
                    ufos.remove(ufo)
                    points -= 1
                    scoreLabel.set_text(f"Score: {points}", 30, (255, 255, 255))

        for ufo in ufos:
            for bullet in bullets:
                if bullet.rect.colliderect(ufo.rect):
                    ufo.rect.x = randint(0, sW - ufo.rect.width)
                    ufo.rect.y = randint(-200, -70)
                    bullets.remove(bullet)
                    points += 1
                    scoreLabel.set_text(f"Score: {points}", 30, (255, 255, 255))

        if points == 100:
            isWon = True
            finalLabel.set_text("You win!", 25, (255, 255, 255))

    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit()
        elif ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                shoot_sound.play()
                new_bullet = Picture(resource_path("assets/images/bullet.png"), rocket.rect.centerx - 15, rocket.rect.y, 30, 30)
                bullets.append(new_bullet)

    clock.tick(60)
    display.update()

