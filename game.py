import pygame

from standard_player import standard_player
import networks2
from random import choice
from random import randint

class game:
    def __init__(self, player1, player2, disp=True) -> None:
        self.disp = disp

        if self.disp:
            pygame.init()
            self.screen = pygame.display.set_mode([700, 500])
            self.clock = pygame.time.Clock()
        self.running = True

        if player1 == None:
            self.player1 = standard_player(self, 50, 50)
        else:
            self.player1 = standard_player(self, 50, 50, network=player1)

        if player2 == None:
            self.player2 = standard_player(self, 50, 50)
        else:
            self.player2 = standard_player(self, 200, 50, network=player2)

            #weights = networks2.weightloader([10, 15, 15, 4, 4])

        self.entities = []
    def sim(self):
        #screen dimensions
        winner = None
        print("*", end='', flush=True)
        maxtickcount = 4000
        while self.running and maxtickcount > 0:
            maxtickcount -= 1
            # Did the user click the window close button?
            if self.disp:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

            inputs = pygame.key.get_pressed()
            self.player1.event(inputs)

            if self.player1.bot:
                nninputs = self.player1.objdata() + self.player2.objdata()
                self.player1.botmove(nninputs)

            if self.player2.bot:
                nninputs = self.player2.objdata() + self.player1.objdata()
                self.player2.botmove(nninputs)
            
            # Update player positions based on their velocity
            self.player1.update()
            self.player2.update()
            for entity in self.entities:
                entity.update()
            self.entitycheck()


            # Draw on screen
            if self.disp:
                self.screen.fill((255, 255, 255))
                self.player1.draw()
                self.player2.draw()
                for entity in self.entities:
                    entity.draw()
                pygame.display.flip()
                self.clock.tick(500)


            for entity in self.entities:
                if entity.touching(self.player1):
                    winner = self.player2
                    self.running = False
                if entity.touching(self.player2):
                    winner = self.player1
                    self.running = False

        #pygame.quit()
        return winner
    def entitycheck(self):
        for entity in self.entities:
            if entity.dead():
                self.entities.remove(entity)
    def draw(self, color, rectdims):
        pygame.draw.rect(self.screen, color, rectdims) 
def main():
    botcounter = 0
    botweights = []
    while True:
        mygame = game()
        bot = mygame.sim(0)
        if bot:
            botcounter += 1
            botweights.append(bot.weights)
        if botcounter == 100:
            print("loaded")
            break
    
    with open("spitfile.txt", 'w') as f:
        for weights in botweights:
            for mat in weights[:-1]:
                print(*[item for row in mat for item in row], sep=' ', file=f)
            print(*weights[-1], sep=' ', file=f)
            print("SPLIT_HERE", file=f)
def fromfile(infile, outfile):
    bots = [child for parent in networks2.loadbots(infile) for child in networks2.offspring(parent, 9, 0.1)]
    stale = 0
    while True:
        idx1 = randint(0, len(bots) - 1)
        idx2 = randint(0, len(bots) - 1)
        mygame = game((bots[idx1], bots[idx2]), disp=True)
        bot = mygame.sim()
        if bot:
            bot = bot.weights
        if bot is bots[idx1]:
            bots.pop(idx2)
        elif bot is bots[idx2]:
            bots.pop(idx1)
        else:
            bots.pop(choice([idx1, idx2]))
            stale += 1
        print(len(bots))
        if len(bots) == 100:
            break
    print(f"{stale} stalemate games")
    networks2.export(bots, outfile)
        
if __name__ == "__main__":
    #main()
    starting = 481
    while True:
        fromfile(f"gen{starting}.txt", f"gen{starting + 1}.txt")
        starting += 1