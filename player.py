import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        # Load player image
        try:
            self.image = pygame.image.load(os.path.join("Assets", "player.png"))
            # Scale player to appropriate size based on screen size
            player_size = (40, 40)  # Adjust based on game-example.jpg
            self.image = pygame.transform.scale(self.image, player_size)
        except:
            # Create a default rectangle if image not found
            self.image = pygame.Surface((30, 30))
            self.image.fill((0, 255, 0))  # Green color
            
        # Health attributes
        self.max_health = 150
        self.health = self.max_health
        
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Set initial position at bottom center
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        
        # Movement speed
        self.speed = 4
        
        # Bullet properties
        self.bullet_group = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 300  # Minimum time between shots in milliseconds
    
    def update(self):
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Move left/right
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
        
        # Update bullets
        self.bullet_group.update()
        
        # Remove bullets that are off screen
        for bullet in self.bullet_group.copy():
            if bullet.rect.bottom < 0:
                self.bullet_group.remove(bullet)
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullet_group.add(bullet)
            self.last_shot = current_time

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join("Assets", "player-bullet.png"))
            # Scale the bullet image to appropriate size (30% of player size)
            player_size = Player(800, 600).image.get_size()
            bullet_size = (int(player_size[0] * 0.5), int(player_size[1] * 0.5))
            self.image = pygame.transform.scale(self.image, bullet_size)
        except:
            # Create a default rectangle if image not found
            self.image = pygame.Surface((3, 7))
            self.image.fill((255, 255, 255))  # White color
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = -8  # Negative because moving upward
    
    def update(self):
        self.rect.y += self.speed