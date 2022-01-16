import pygame
import sys
import os
import random


pygame.init()


def load_image(name, folder="data", colorkey=None):
    fullname = os.path.join(folder, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


RUN = [load_image('Run (1).png'), load_image('Run (2).png'), load_image('Run (3).png'), load_image('Run (4).png'),
       load_image('Run (5).png'), load_image('Run (6).png'), load_image('Run (7).png'), load_image('Run (8).png')]

JUMP = [load_image('Jump (1).png'), load_image('Jump (2).png'), load_image('Jump (3).png'), load_image('Jump (4).png'),
        load_image('Jump (5).png'), load_image('Jump (6).png'), load_image('Jump (7).png'), load_image('Jump (8).png'),
        load_image('Jump (9).png'), load_image('Jump (10).png'), load_image('Jump (11).png'), load_image('Jump (12).png')]

for i in range(len(JUMP)):
    JUMP[i] = pygame.transform.scale(JUMP[0], (136, 94))

for i in range(len(RUN)):
    RUN[i] = pygame.transform.scale(RUN[0], (136, 94))

TRACE = load_image('Track.png')


class Cloud(pygame.sprite.Sprite):
    def __init__(self, width, height, *group):
        super().__init__(*group)
        self.image = load_image('cloud1.png')
        self.rect = self.image.get_rect()
        print(self.rect)
        print(width - self.rect.width, width)
        print(0, self.rect.height // 4)
        self.rect.x = random.randrange(350, 700)
        self.rect.y = random.randrange(0, 100)
        self.count = 0

    def update(self, screen):
        if self.count % 10 == 0:
            self.rect = self.rect.move(random.randrange(3) - 1,
                                       random.randrange(3) - 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.count += 1


class Sun(pygame.sprite.Sprite):
    def __init__(self, width, height, *group):
        super().__init__(*group)
        self.image = load_image('sun_shiny.png')
        self.rect = self.image.get_rect()
        print(self.rect)
        print(width - self.rect.width, width)
        print(0, self.rect.height // 4)
        self.rect.x = 680
        self.rect.y = 10
        self.count = 0

    def update(self, screen):
        if self.count % 10 == 0:
            self.rect = self.rect.move(random.randrange(3) - 1,
                                       random.randrange(3) - 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.count += 1


class Dino:
    XPOS = 80
    YPOS = 223
    JUMPSPEED = 8.5

    def __init__(self, img=RUN[0]):
        self.image = img
        self.isrun = True
        self.isjump = False
        self.speed = self.JUMPSPEED
        self.rect = pygame.Rect(self.XPOS, self.YPOS, img.get_width(), img.get_width())
        self.steps = 0

    def update(self):
        if self.isrun:
            self.run()
        if self.isjump:
            self.jump()
        if self.steps >= 40:
            self.steps = 0

    def run(self):
        self.image = RUN[self.steps // 5]
        self.rect.x = self.XPOS
        self.rect.y = self.YPOS
        self.steps += 5

    def jump(self):
        self.image = JUMP[self.steps // 5]
        if self.isjump:
            self.rect.y -= self.speed * 4
            self.speed -= 0.8
        if self.speed <= - self.JUMPSPEED:
            self.isjump = False
            self.isrun = True
            self.speed = self.JUMPSPEED

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))


class App:
    def __init__(self):
        pygame.init()
        self.height = 400
        self.width = 800
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Dino')
        self.fps = 50
        self.fon = TRACE
        self.points = 0
        self.gamespeed = 20

    def terminate(self):
        pygame.quit()
        sys.exit()

    def get_score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.gamespeed += 1
        self.points_text = f'Points: {self.points}'
        return self.points_text

    def run_game(self):
        text = self.get_score()
        dinos = [Dino()]
        clock = pygame.time.Clock()
        run = True
        clouds = pygame.sprite.Group()
        suns = pygame.sprite.Group()
        sun = Sun(800, 400, suns)
        for i in range(3):
            Cloud(800, 400).add(clouds)
            Cloud(800, 400, clouds)
        font = pygame.font.Font(None, 30)
        text_coord = 50
        string_rendered = font.render(text, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                    sys.exit()
            # update

            # render
            self.screen.fill(pygame.Color('white'))
            for dino in dinos:
                dino.update()
                dino.draw(self.screen)

            key = pygame.key.get_pressed()

            for i, dino in enumerate(dinos):
                if key[pygame.K_SPACE]:
                    dino.isjump = True
                    dino.isrun = False
            self.screen.blit(self.fon, (0, 300))
            clouds.update(self.screen)
            sun.update(self.screen)
            self.screen.blit(string_rendered, intro_rect)
            clock.tick(self.fps)
            pygame.display.update()


if __name__ == '__main__':
    app = App()
    app.run_game()
