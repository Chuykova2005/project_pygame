import os
import sys
import pygame
<<<<<<< HEAD

##
=======
import pygame_gui


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
        self.rect = pygame.Rect(0,  0, sheet.get_width() // columns,
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


>>>>>>> develop/elena
class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 600
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
<<<<<<< HEAD
        pygame.display.set_caption('Mario')
        self.fps = 50
=======
>>>>>>> develop/elena

    def terminate(self):
        pygame.quit()
        sys.exit()

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

<<<<<<< HEAD
    def run_game(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
            # update

            # render
            self.screen.fill(pygame.Color('blue'))
            pygame.display.flip()
            self.clock.tick(self.fps)
=======
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
            time_delta = self.clock.tick(60) / 1000.0
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
>>>>>>> develop/elena


if __name__ == '__main__':
    app = App()
<<<<<<< HEAD
    app.run_game()
=======
    app.start_window()
>>>>>>> develop/elena
