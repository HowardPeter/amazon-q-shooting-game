import pygame
import sys
from player import Player
from enemy import EnemyManager

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 150, 50)
LIGHT_GREEN = (70, 170, 70)

# Game states
START_SCREEN = "start"
PLAYING = "playing"
TUTORIAL = "tutorial"
FINISH_SCREEN = "finish"

class Button:
    def __init__(self, x, y, width, height, text, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = GREEN
        self.hover_color = LIGHT_GREEN
        
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)  # Border
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        
        # Load background
        try:
            self.background = pygame.image.load("Assets/background.jpg").convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            print("Warning: Could not load background image 'Assets/background.png'")
            self.background = None
        
        # Game state
        self.state = START_SCREEN
        
        # Create game objects
        self.player = None
        self.enemy_manager = None
        
        # Score
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Health bar colors
        self.HEALTH_BAR_GREEN = (0, 255, 0)
        self.HEALTH_BAR_RED = (255, 0, 0)
        self.HEALTH_BAR_BORDER = (255, 255, 255)
        
        # Create buttons
        button_width = 200
        button_height = 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        # Start screen buttons
        self.start_button = Button(center_x, SCREEN_HEIGHT // 2, 
                                 button_width, button_height, "Start")
        self.tutorial_button = Button(center_x, SCREEN_HEIGHT // 2 + 70, 
                                    button_width, button_height, "Tutorial")
        
        # Finish screen buttons
        self.play_again_button = Button(center_x, SCREEN_HEIGHT // 2 + 70, 
                                      button_width, button_height, "Play Again")
        self.home_button = Button(center_x, SCREEN_HEIGHT // 2 + 140, 
                                button_width, button_height, "Home")
    
    def reset_game(self):
        """Reset the game state to start a new game"""
        self.score = 0
        self.player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.enemy_manager = EnemyManager(SCREEN_WIDTH)
        self.state = PLAYING

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == START_SCREEN:
                    if self.start_button.is_clicked(mouse_pos):
                        self.reset_game()
                    elif self.tutorial_button.is_clicked(mouse_pos):
                        self.state = TUTORIAL
                elif self.state == TUTORIAL:
                    # Any click in tutorial returns to start screen
                    self.state = START_SCREEN
                elif self.state == FINISH_SCREEN:
                    if self.play_again_button.is_clicked(mouse_pos):
                        self.reset_game()
                    elif self.home_button.is_clicked(mouse_pos):
                        self.state = START_SCREEN
            elif event.type == pygame.KEYDOWN and self.state == PLAYING:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
        return True
    
    def update(self):
        if self.state == PLAYING:
            # Update game objects
            self.player.update()
            self.enemy_manager.update()
            
            # Check for collisions between player bullets and enemies
            collisions = pygame.sprite.groupcollide(
                self.player.bullet_group,
                self.enemy_manager.enemy_group,
                True,  # Delete the bullet
                True   # Delete the enemy
            )
            
            # Update score
            self.score += len(collisions)
            
            # Check for collisions between enemy bullets and player
            if pygame.sprite.spritecollide(self.player, self.enemy_manager.bullet_group, True):
                # Player hit by enemy bullet - reduce health by 30
                self.player.health = max(0, self.player.health - 30)
                
            # Check if player is dead
            if self.player.health <= 0:
                self.state = FINISH_SCREEN
            
            # Check if all enemies are defeated
            if len(self.enemy_manager.enemy_group) == 0:
                self.state = FINISH_SCREEN
    
    def draw(self):
        # Draw background or fill with black if no background image
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        if self.state == START_SCREEN:
            # Draw title
            title = self.big_font.render("SPACE SHOOTER", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            self.screen.blit(title, title_rect)
            
            # Draw buttons
            self.start_button.draw(self.screen)
            self.tutorial_button.draw(self.screen)
            
        elif self.state == TUTORIAL:
            # Draw tutorial text
            tutorial_lines = [
                "Welcome to Space Shooter!",
                "",
                "Controls:",
                "- Use LEFT/RIGHT arrows to move",
                "- Press SPACE to shoot",
                "",
                "Objective:",
                "- Destroy all enemy ships",
                "- Avoid enemy bullets",
                "",
                "Click anywhere to return"
            ]
            
            y = 100
            for line in tutorial_lines:
                # Use green color for the "Click anywhere to return" line
                color = GREEN if line == "Click anywhere to return" else WHITE
                text = self.font.render(line, True, color)
                rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(text, rect)
                y += 40
                
        elif self.state == PLAYING:
            # Draw player and bullets
            self.screen.blit(self.player.image, self.player.rect)
            self.player.bullet_group.draw(self.screen)
            
            # Draw enemies and their bullets
            self.enemy_manager.enemy_group.draw(self.screen)
            self.enemy_manager.bullet_group.draw(self.screen)
            
            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
            
            # Draw health bar
            health_bar_width = 200
            health_bar_height = 20
            health_bar_pos = (10, 10)  # Position in the left corner
            
            # Draw border
            pygame.draw.rect(self.screen, self.HEALTH_BAR_BORDER, 
                           (health_bar_pos[0] - 2, health_bar_pos[1] - 2,
                            health_bar_width + 4, health_bar_height + 4))
            
            # Draw red background
            pygame.draw.rect(self.screen, self.HEALTH_BAR_RED,
                           (health_bar_pos[0], health_bar_pos[1],
                            health_bar_width, health_bar_height))
            
            # Draw green health
            health_width = int((self.player.health / self.player.max_health) * health_bar_width)
            if health_width > 0:
                pygame.draw.rect(self.screen, self.HEALTH_BAR_GREEN,
                               (health_bar_pos[0], health_bar_pos[1],
                                health_width, health_bar_height))
                
        elif self.state == FINISH_SCREEN:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(128)  # 50% transparency
            self.screen.blit(overlay, (0, 0))
            
            # Draw game over text
            if len(self.enemy_manager.enemy_group) == 0:
                title_text = "VICTORY!"
            else:
                title_text = "GAME OVER"
            
            game_over_text = self.big_font.render(title_text, True, WHITE)
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            
            # Center the text on screen
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # Draw the text
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(final_score_text, final_score_rect)
            
            # Draw buttons
            self.play_again_button.draw(self.screen)
            self.home_button.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()