import pygame
from standard_player import standard_player










def main():
    pygame.init()

    #screen dimensions
    screen = pygame.display.set_mode([500, 500])

    # Run until the user asks to quit
    running = True
    player1 = standard_player(screen, 50, 50)
    player2 = standard_player(screen, 200, 50)
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif event.type == pygame.KEYDOWN:
            #     player1.event(event.key)

        inputs = pygame.key.get_pressed()
        player1.event(inputs)

        # Fill the background with white
        screen.fill((255, 255, 255))
        
        # Update player positions based on their velocity
        player1.update()
        player2.update()

        # Draw on screen
        player1.draw()
        player2.draw()

        # Flip the display
        pygame.display.flip()
        pygame.time.wait(5)

    # Done! Time to quit.
    pygame.quit()

if __name__ == "__main__":
    main()