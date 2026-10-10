import pygame


class Counter:

    def __init__(self, count, position, police_size, screen):
        self.count = count
        self.pos = position
        self.font = pygame.font.SysFont(None, police_size)
        self.screen = screen

    def update(self, count):
        self.count = count

    def blit(self):
        image = self.font.render(str(self.count), True, (255, 255, 255))
        self.screen.blit(image, self.pos)


class Clickable_Button:

    def __init__(self, position, size, button_sprite, button_clicked_sprite, screen):
        self.pos = position
        self.size = size
        self.click = False
        self.button_image = pygame.transform.scale(
            pygame.image.load(button_sprite).convert(), self.size
        )
        self.button_clicked_image = pygame.transform.scale(
            pygame.image.load(button_clicked_sprite).convert(), self.size
        )
        self.screen = screen

    def event(self):

        mouse_pos = pygame.mouse.get_pos()
        if (
            pygame.mouse.get_pressed()[0] == True
            and self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0]
            and self.pos[1] < mouse_pos[1] < self.pos[1] + self.size[1]
        ):
            self.click = True
            return True
        elif pygame.mouse.get_pressed()[0] == False and self.click == True:
            return False
        else:
            self.click = False
            return True

    def blit(self):
        if self.click == False:
            self.screen.blit(self.button_image, self.pos)
        elif self.click == True:
            self.screen.blit(self.button_clicked_image, self.pos)


class Input_Box:

    def __init__(
        self, box_position, text_position, size, box_sprite, screen, text=None
    ):

        self.screen = screen
        self.size = size
        self.click = False
        self.text_pos = text_position
        self.box_pos = box_position
        self.font = pygame.font.SysFont(None, 48)
        if text == None:
            self.text = ""
        else:
            self.text = text
        self.empty_box = pygame.transform.scale(
            pygame.image.load(box_sprite).convert(), self.size
        )

    def input(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

        return self.text

    def event(self):

        mouse_pos = pygame.mouse.get_pos()
        if (
            pygame.mouse.get_pressed()[0] == True
            and self.box_pos[0] < mouse_pos[0] < self.box_pos[0] + self.size[0]
            and self.box_pos[1] < mouse_pos[1] < self.box_pos[1] + self.size[1]
        ):
            self.click = True
            return True
        elif pygame.mouse.get_pressed()[0] == False and self.click == True:
            return False
        else:
            self.click = False
            return True

    def blit(self):
        image = self.font.render(self.text, True, (255, 255, 255))
        self.screen.blit(self.empty_box, self.box_pos)
        self.screen.blit(
            image,
            (
                self.box_pos[0] - (image.get_width() / 2) + (self.size[0] / 2),
                self.box_pos[1] + 10,
            ),
        )


class Text_Box:

    def __init__(self, position, size, text_pos, box_sprite, text, police, screen):
        self.pos = position
        self.size = size
        self.text = Counter(text, text_pos, police, screen)
        self.box_image = pygame.transform.scale(
            pygame.image.load(box_sprite).convert(), self.size
        )
        self.screen = screen

    def blit(self):
        self.screen.blit(self.box_image, self.pos)
        self.text.blit()
