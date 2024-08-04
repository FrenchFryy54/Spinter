import pygame

class standard_player:
    def __init__(self, screen, x, y) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

        self.jumping = False
    def draw(self):
        pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, 20, 20))
    def event(self, inputs):
        if inputs[pygame.K_RIGHT]:
            self.vx += 0.2
        elif inputs[pygame.K_LEFT]:
            self.vx -= 0.2
        elif inputs[pygame.K_UP] and not self.jumping:
            self.vy -= 5
            self.jumping = True
    def update(self):
        self.vx *= 0.85
        self.x += self.vx

        self.vy += 0.1
        self.y += self.vy

        if self.y > 500 - 20:
            self.y = 500 - 20
            self.vy = 0
            self.jumping = False