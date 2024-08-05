
class attack:
    def __init__(self, game, x, y, vx) -> None:
        self.game = game
        self.x = x
        self.y = y
        self.vx = vx

        self.time = 500
    def draw(self):
        self.game.draw((255, 0, 0), (self.x, self.y, 20, 20))

    def update(self):
        self.time -= 5
        self.x += self.vx
    def dead(self):
        return self.time <= 0
    
    def touching(self, player):
        if player.x + 30 < self.x:
            return False
        if self.x + 20 < player.x:
            return False
        if player.y + 30 < self.y:
            return False
        if self.y + 20 < player.y:
            return False
        return True

