from attack import attack
import networks2
import pygame

class standard_player:
    def __init__(self, game, x, y, network = None) -> None:
        self.game = game

        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

        self.jumping = False

        self.attack_delay = 2000

        self.bot = network is not None
        if self.bot:
            self.weights = network
    def draw(self):
        self.game.draw((0, 255, 0), (self.x, self.y, 30, 30))

    def botmove(self, inputs):
        outs = networks2.feed(inputs, self.weights)

        if round(outs[0]):
            self.vx += 0.2
        if round(outs[1]):
            self.vx -= 0.2
        if round(outs[2]) and not self.jumping:
            self.vy -= 6
            self.jumping = True
        print(outs[3])
        if round(outs[3]) and self.attack_delay < 0:
            self.attack_delay = 2000

            # summon an attack
            newattack = attack(self.game, (self.x + 5) + 40 * [-1, 1][self.vx > 0], (self.y + 5), 2 * [-1, 1][self.vx > 0])
            self.game.entities.append(newattack)

    def event(self, inputs):
        if inputs[pygame.K_RIGHT]:
            self.vx += 0.2
        if inputs[pygame.K_LEFT]:
            self.vx -= 0.2
        if inputs[pygame.K_UP] and not self.jumping:
            self.vy -= 6
            self.jumping = True
        if inputs[pygame.K_DOWN] and self.attack_delay < 0:
            self.attack_delay = 2000

            # summon an attack
            newattack = attack(self.game, (self.x + 5) + 40 * [-1, 1][self.vx > 0], (self.y + 5), 2 * [-1, 1][self.vx > 0])
            self.game.entities.append(newattack)
    def objdata(self):
        return [self.x / 100, self.y / 100, self.vx, self.vy, self.attack_delay * (self.attack_delay > 0) * 0.001]
    def update(self):
        self.vx *= 0.85
        self.x += self.vx

        self.vy += 0.1
        self.y += self.vy

        if self.x < 0:
            self.x = 0
        if self.x > 700 - 30:
            self.x = 700 - 30

        self.attack_delay -= 5

        if self.y > 500 - 30:
            self.y = 500 - 30
            self.vy = 0
            self.jumping = False

        