import pygame,random

pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangle")

#Define FPS
FPS = 60
clock = pygame.time.Clock()

#Define classes
class Game():
    
    def __init__(self , player , monster_group):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.monster_group = monster_group

        # Set sounds
        self.next_level_sound = pygame.mixer.Sound(r"monster_wrangler_assets\\next_level.wav")

        # Set fonts
        self.font = pygame.font.Font(r"monster_wrangler_assets\Abrushow.ttf" , 24)

        # Set images
        blue_image = pygame.image.load(r"monster_wrangler_assets\blue_monster.png")
        green_image = pygame.image.load(r"monster_wrangler_assets\\green_monster.png")
        purple_image = pygame.image.load(r"monster_wrangler_assets\\purple_monster.png")
        yellow_image = pygame.image.load(r"monster_wrangler_assets\\yellow_monster.png")
        # Monster type is an int 0 -> blue , 1 -> green , 2 -> purple , 3 -> yellow
        self.target_monster_images = [blue_image , green_image , purple_image , yellow_image]

        self.target_monster_type = random.randint(0 , 3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH // 2
        self.target_monster_rect.top = 30



    # Update the game
    def update(self):
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0 

        # Check for collision
        self.check_collisions()

    # Draw HUD and others to the displays
    def draw(self):
        
        # Set colors
        WHITE = (255,255,255)
        BLUE = (20,176,235)
        GREEN = (87,201,47)
        PURPLE = (226 , 73 , 243)
        YELLOW = (243 , 157 , 20)

        #Add the colors to target monster
        colors = [BLUE , GREEN , PURPLE , YELLOW]

        # Set text
        catch_text = self.font.render("Current Catch" , True , WHITE)
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.centerx = WINDOW_WIDTH // 2
        catch_text_rect.top = 5

        score_text = self.font.render(f"Score: {self.score}" , True , WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (5 , 5)

        lives_text = self.font.render(f"Lives: {self.player.lives}" , True , WHITE)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (5 , 35)

        round_text = self.font.render(f"Current Rounds: {self.round_number}" , True , WHITE)
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (5 , 65)

        time_text = self.font.render(f"Round Time: {self.round_time}" , True , WHITE)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (WINDOW_WIDTH - 10 , 5)

        warp_text = self.font.render(f"Warps: {self.player.warps}" , True , WHITE)
        warp_text_rect = warp_text.get_rect()
        warp_text_rect.topright = (WINDOW_WIDTH - 10 , 35)

        display_surface.blit(catch_text , catch_text_rect)
        display_surface.blit(score_text , score_text_rect)
        display_surface.blit(lives_text , lives_text_rect)
        display_surface.blit(round_text , round_text_rect)
        display_surface.blit(time_text , time_text_rect)
        display_surface.blit(warp_text , warp_text_rect)
        display_surface.blit(self.target_monster_image , self.target_monster_rect)

        pygame.draw.rect(display_surface , colors[self.target_monster_type] , (WINDOW_WIDTH // 2 - 32 , 30 , 64, 64) , 2)
        pygame.draw.rect(display_surface , colors[self.target_monster_type] , (0 , 100 , WINDOW_WIDTH , WINDOW_HEIGHT - 200) , 2)
    
    # check collision btw monster and player
    def check_collisions(self):
        collide_monster = pygame.sprite.spritecollideany(self.player , self.monster_group)

        if collide_monster:
            
            if collide_monster.type == self.target_monster_type:
                self.score += 100 * self.round_number

                # Remove the monster
                collide_monster.remove(self.monster_group)
                if (self.monster_group):
                    # There are more monsters to catch
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    # Round complete
                    self.player.reset()
                    self.start_new_round()
            else:
                # Caught the wrong monster
                self.player.die_sound.play()
                self.player.lives -= 1

                if self.player.lives < 0:
                    self.pause_game(f"Final Score: {self.score}" , "Press 'Enter' to play again")
                    self.reset_game()

                self.player.reset()

    # Start new rounds
    def start_new_round(self):
        
        # Provide score bonus based on how quickly the player finish
        self.score += int(10000*self.round_number/(1 + self.round_time))

        # Reset the values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1

        # Remove any remainning monsters from a game reset
        for monster in self.monster_group:
            self.monster_group.remove(monster)

        # Add monsters to the monster group
        for i in range(self.round_number):
            self.monster_group.add(Monster(random.randint(0 , WINDOW_WIDTH - 64), random.randint(100 , WINDOW_HEIGHT - 164) , self.target_monster_images[0] , 0))
            self.monster_group.add(Monster(random.randint(0 , WINDOW_WIDTH - 64), random.randint(100 , WINDOW_HEIGHT - 164) , self.target_monster_images[1] , 1))
            self.monster_group.add(Monster(random.randint(0 , WINDOW_WIDTH - 64), random.randint(100 , WINDOW_HEIGHT - 164) , self.target_monster_images[2] , 2))
            self.monster_group.add(Monster(random.randint(0 , WINDOW_WIDTH - 64), random.randint(100 , WINDOW_HEIGHT - 164) , self.target_monster_images[3] , 3))

        self.choose_new_target()

        self.next_level_sound.play()

    # choose a new target monster for player
    def choose_new_target(self):
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image
    
    # Pause the game
    def pause_game(self , main_text , sub_text):

        global running

        WHITE = (255,255,255)

        # create main text
        main_text = self.font.render(main_text, True , WHITE)
        main_text_rect = main_text.get_rect()
        main_text_rect.center = (WINDOW_WIDTH // 2 , WINDOW_HEIGHT // 2)

        # create the sub text
        sub_text = self.font.render(sub_text , True , WHITE)
        sub_text_rect = sub_text.get_rect()
        sub_text_rect.center = (WINDOW_WIDTH // 2 , WINDOW_HEIGHT // 2 + 64)

        #display the pause text
        display_surface.fill((0,0,0))
        display_surface.blit(main_text , main_text_rect)
        display_surface.blit(sub_text , sub_text_rect)
        pygame.display.update()

        # Pause the game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False

    # reset the game
    def reset_game(self):
        
        self.score = 0
        self.round_number = 0

        self.player.lives = 5
        self.player.warps = 2
        self.player.reset()

        self.start_new_round()


class Player(pygame.sprite.Sprite):

    #Initialize the player
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"monster_wrangler_assets\\knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 5
        self.warps = 2
        self.velocity = 8

        self.catch_sound = pygame.mixer.Sound(r"monster_wrangler_assets\\catch.wav")
        self.die_sound = pygame.mixer.Sound(r"monster_wrangler_assets\die.wav")
        self.warp_sound = pygame.mixer.Sound(r"monster_wrangler_assets\warp.wav")

    # Update the player
    def update(self):
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT - 100:
            self.rect.y += self.velocity
        

    # Warp the player to safe zone
    def warp(self):
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = WINDOW_HEIGHT
    
    # Resets player position
    def reset(self):
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT



class Monster(pygame.sprite.Sprite):
    """To create enemy monster objects"""

    # Initialize monster
    def __init__(self , x , y , image , monster_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)

        # Monster type is an int 0 -> blue , 1 -> green , 2 -> purple , 3 -> yellow
        self.type = monster_type

        # set random motion
        self.dx = random.choice([-1 , 1])
        self.dy = random.choice([-1 , 1])
        self.velocity = random.randint(1 , 5)

    # Update the monster
    def update(self):
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx *= -1
        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            self.dy *= -1


# Create player group
my_player_group = pygame.sprite.Group()
player = Player()
my_player_group.add(player)


# Create monster group
my_monster_group = pygame.sprite.Group()



# Create game group
my_game = Game(player , my_monster_group)
my_game.pause_game("Monster Wrangler" , "Press 'Enter' to start the game!")
my_game.start_new_round()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.warp()

    # Fill the screen
    display_surface.fill((0,0,0))

    # Update and draw player
    my_player_group.update()
    my_player_group.draw(display_surface)

    # Update and draw monster
    my_monster_group.update()
    my_monster_group.draw(display_surface)

    # Update the game object
    my_game.update()
    my_game.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()