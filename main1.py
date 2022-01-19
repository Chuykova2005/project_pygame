import os
import random
import sys
import pygame
import pygame_gui

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

PTERO = [load_image('ptero1.png'), load_image('ptero2.png'), load_image('ptero3.png'), load_image('ptero4.png'),
         load_image('ptero5.png'), load_image('ptero6.png'), load_image('ptero7.png')]

for i in range(len(PTERO)):
    PTERO[i] = pygame.transform.scale(PTERO[i], (100, 84))


class AnimatedDragon(pygame.sprite.Sprite):
    def __init__(self, app, sheet, columns, rows, x, y):
        super().__init__(app.anim_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.rect.w = self.rect.w * 4
        self.rect.h = self.rect.h * 4
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (self.rect.w, self.rect.h))
        self.rect = self.rect.move(x, y)
        self.speed = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.speed += 1
        if self.speed == 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (self.rect.w, self.rect.h))
            self.speed = 0


JUMP = [load_image('Jump (1).png'), load_image('Jump (2).png'), load_image('Jump (3).png'), load_image('Jump (4).png'),
        load_image('Jump (5).png'), load_image('Jump (6).png'), load_image('Jump (7).png'), load_image('Jump (8).png'),
        load_image('Jump (9).png'), load_image('Jump (10).png'), load_image('Jump (11).png'),
        load_image('Jump (12).png')]

for i in range(len(JUMP)):
    JUMP[i] = pygame.transform.scale(JUMP[i], (136, 94))

for i in range(len(RUN)):
    RUN[i] = pygame.transform.scale(RUN[i], (136, 94))

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


class Ptero(pygame.sprite.Sprite):
    """класс птеродактиля"""
    XPOS = 700
    YPOS = 20

    def __init__(self, app, img=PTERO[0]):
        super().__init__(app.herogroup)
        self.image = img
        self.isrun = True
        self.isjump = False
        self.rect = pygame.Rect(self.XPOS, self.YPOS, img.get_width(), img.get_width())
        self.steps = 0
        self.jx, self.jy = 0, 0

    def fly(self):
        self.image = PTERO[self.steps // 5]
        self.rect.x = self.XPOS
        self.rect.y = [10, 10, 20, 60, 60, 60, 50][self.steps // 5] + 1
        self.steps += 1
        if self.steps >= 35:
            self.steps = 0
        app.screen.blit(self.image, (self.rect.x, self.rect.y))


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


class Dino(pygame.sprite.Sprite):
    XPOS = 80
    YPOS = 223
    JUMP_VEL = 6.5
    JUMPSPEED = 8.5

    def __init__(self, app, img=RUN[0]):
        super().__init__(app.herogroup)
        self.image = img
        self.isrun = True
        self.isjump = False
        self.speed = self.JUMPSPEED
        self.rect = pygame.Rect(self.XPOS, self.YPOS, img.get_width(), img.get_width())
        self.steps = 0
        self.jump_vel = self.JUMP_VEL
        self.jx, self.jy = 0, 0

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
        self.steps += 1

    def jump(self):
        self.steps += 1
        self.image = JUMP[self.steps // 5]
        if self.isjump:
            self.rect.y -= self.speed * 0.6
            self.speed -= 0.1
        if self.speed <= - self.JUMPSPEED:
            self.isjump = False
            self.isrun = True
            self.speed = self.JUMPSPEED

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))


class Obstacles(pygame.sprite.Sprite):
    images_obstracle = {'1': 'cactus1.png',
                        '2': 'cactus2.png',
                        '3': 'cactus3.png',
                        '4': 'rocks2.png',
                        '5': 'rocks3.png'
                        }

    def __init__(self, app, type, pos):
        super().__init__(app.all_obstacles)
        self.app = app
        self.type = Obstacles.images_obstracle[type]
        self.image = self.app.load_image(self.type)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1] - self.rect.h
        print(self.rect)

    def update(self):
        if self.rect.x < 0:
            self.kill()
        else:
            self.rect.x -= 1


class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 400
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.all_obstacles = pygame.sprite.Group()
        self.myeventtype = 30
        pygame.display.set_caption('Dino')
        self.fps = 60
        self.fon = TRACE
        self.points = 0
        self.gamespeed = 20
        self.herogroup = pygame.sprite.Group()
        self.load_sounds()
        self.best_score = []

    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_sounds(self):
        """загрузка звуков для спецэффектов"""
        self.s_jump = pygame.mixer.Sound('data/jump.ogg') # прыжок
        self.s_dead = pygame.mixer.Sound('data/dead.mp3')
        self.s_fanfar = pygame.mixer.Sound('data/fanfar.mp3')  # фанфары
        self.s_fon = pygame.mixer.Sound('data/fon_music.mp3')

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def get_score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.gamespeed += 1
        self.points_text = f'Points: {self.points}'
        return self.points_text

    def generate_level(self, move):
        fon = self.load_image('gradient.jpg')
        self.rect_fon = fon.get_rect()
        self.rect_fon.bottom = self.height
        self.rect_fon.x = move
        self.screen.fill(pygame.Color('lightblue'))
        # self.screen.blit(fon, self.rect_fon)

    def run_game(self):
        self.s_fon.play()
        pygame.time.set_timer(self.myeventtype, 1000)

        self.dinos = [Dino(self)]

        run = True
        # self.dino = Dino(self)
        move_fon = 0
        clouds = pygame.sprite.Group()
        suns = pygame.sprite.Group()
        sun = Sun(800, 400, suns)
        for i in range(3):
            Cloud(800, 400).add(clouds)
            Cloud(800, 400, clouds)
        font = pygame.font.Font(None, 30)
        self.ptero = Ptero(self)
        text_coord = 50
        while run:
            # fon2 = pygame.transform.scale(self.load_image('grass2.png'), (600, 124))
            # self.screen.blit(fon2, (0, self.height - 124))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                key = pygame.key.get_pressed()
                for i, dino in enumerate(self.dinos):
                    if key[pygame.K_SPACE]:
                        self.s_jump.play()
                        dino.isjump = True
                        dino.isrun = False

                if event.type == self.myeventtype:
                    type = random.choice(['1', '2', '3', '4', '5'])
                    print('type', type)
                    Obstacles(self, type, (self.width, 325))
                    pygame.time.set_timer(self.myeventtype, random.randrange(1000, 15000, 1000))
            text = self.get_score()
            string_rendered = font.render(text, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            if move_fon > -150:
                move_fon -= 1
            else:
                move_fon = 0

            t = pygame.sprite.spritecollide(self.dinos[0], self.all_obstacles, False,
                                            pygame.sprite.collide_rect_ratio(0.5))
            if t:
                print('crash')
                self.s_fon.stop()
                self.over_game()
                return
            self.generate_level(move_fon)
            self.herogroup.draw(self.screen)
            self.all_obstacles.draw(self.screen)
            for dino in self.dinos:
                dino.update()
                dino.draw(self.screen)
            clouds.update(self.screen)
            sun.update(self.screen)
            self.ptero.fly()
            self.screen.blit(string_rendered, intro_rect)
            self.all_obstacles.update()
            self.screen.blit(load_image('Track.png'), (0, 300))
            # self.herogroup.update()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def start_window(self):
        manager = pygame_gui.UIManager((self.width, self.height))
        btn_run = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.height - 50), (self.width, 50)),
            text='start game',
            manager=manager,
        )
        self.anim_sprites = pygame.sprite.Group()
        drag = AnimatedDragon(self, self.load_image('animdrag.png'), 8, 2, self.width // 2 - 60, self.height // 2 - 50)
        self.anim_flag = False
        screen2 = pygame.Surface(self.screen.get_size())
        intro_text = ["", "DRAGON RACE", "",
                      "Правила игры",
                      "Если в правилах несколько строк,",
                      "приходится выводить их построчно"]

        fon = pygame.transform.scale(self.load_image('fon.jpg'), (self.width, self.height))
        screen2.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 90
            text_coord += intro_rect.height
            screen2.blit(string_rendered, intro_rect)

        while True:
            time_delta = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEMOTION:
                    if self.width // 2 - 60 < event.pos[0] < self.width \
                            and self.height // 2 - 50 < event.pos[1] < self.height:
                        self.anim_flag = True
                    else:
                        self.anim_flag = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == btn_run:
                            print('Вызвать основной цикл игры')
                            return
                manager.process_events(event)
            manager.update(time_delta)
            self.screen.fill(pygame.Color('#7512fa'))

            self.screen.blit(screen2, (0, 0))
            self.anim_sprites.draw(self.screen)
            if self.anim_flag:
                self.anim_sprites.update()
            manager.draw_ui(self.screen)
            pygame.display.flip()

    def over_game(self):
        self.s_dead.play()
        self.screen.blit(load_image('gradient.jpg'), (0, 0))
        self.best_score.append(self.points)
        best_res = max(self.best_score)
        intro_text = ["Вы проиграли",
                      'Количество набранных очков:',
                      f'{self.points}',
                      f'Лучший результат: {best_res}',
                      'Нажмите на экран чтобы продолжить']
        self.points = 0
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 90
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        # update

            # render

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    for obstacle in self.all_obstacles:
                        obstacle.kill()
                    self.dinos[0].kill()
                    self.ptero.kill()
                    self.run_game()
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    app = App()
    app.start_window()
    app.run_game()
