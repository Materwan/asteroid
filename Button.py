import pygame

class Button:
    
    def __init__(self, image, image_size, pos, text_input, color, font):
        self.x_size = image_size[0]
        self.y_size = image_size[1]
        self.image = pygame.transform.scale(image, (self.x_size, self.y_size))
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.font = font
        self.color = color
        self.text = self.font.render(text_input, True, self.color)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.text_rect = self.text.get_rect(center=(self.pos_x, self.pos_y))
        
    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
    def clic(self, image):
        self.image = pygame.transform.scale(image, (self.x_size, self.y_size))
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
    
    def update_text_input(self, screen, text_input, font):
        text = font.render(text_input, True, self.color)
        text_rect = text.get_rect(center=(self.pos_x, self.pos_y))
        screen.blit(self.image, self.rect)
        screen.blit(text, text_rect)
    
    def get_mouse_on(self, mouse_pos):
        if (self.pos_x - self.x_size / 2) < mouse_pos[0] < (self.pos_x + self.x_size / 2) and (self.pos_y - self.y_size / 2) < mouse_pos[1] < (self.pos_y + self.y_size / 2):
            mouse_on = True
        else:
            mouse_on = False
        return mouse_on