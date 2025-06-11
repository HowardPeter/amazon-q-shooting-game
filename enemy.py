import pygame
import os
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join("Assets", "enemy.png"))
            # Scale enemy to appropriate size based on screen size
            enemy_size = (40, 40)  # Adjust based on game-example.jpg
            self.image = pygame.transform.scale(self.image, enemy_size)
        except:
            # Create a default rectangle if image not found
            self.image = pygame.Surface((25, 25))
            self.image.fill((255, 0, 0))  # Red color
        
        self.rect = self.image.get_rect()
        
        # Set fixed position based on grid
        self.rect.x = x
        self.rect.y = y
        
        # Movement properties
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 3      # Horizontal movement speed
        self.start_x = x    # Store initial x position
        self.move_range = 100  # Maximum distance to move from start position
        
        # Shooting properties
        self.shoot_delay = 10000  # 10 seconds between shots
        # Add random initial delay to prevent synchronized shooting
        current_time = pygame.time.get_ticks()
        self.last_shot = current_time - random.randint(0, self.shoot_delay)
    
    def update(self):
        # Move horizontally within the defined range
        self.rect.x += self.speed * self.direction
        
        # Check if we've moved too far from the start position
        distance_moved = abs(self.rect.x - self.start_x)
        if distance_moved >= self.move_range:
            # Reverse direction
            self.direction *= -1
            # Adjust position to exactly at the range limit
            if self.direction < 0:
                self.rect.x = self.start_x + self.move_range
            else:
                self.rect.x = self.start_x - self.move_range
    
    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            return True
        return False

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join("Assets", "enemy-bullet.png"))
            # Scale bullet to appropriate size (30% of enemy size)
            enemy_size = (40, 40)  # Same as enemy size defined above
            bullet_size = (int(enemy_size[0] * 0.3), int(enemy_size[1] * 0.3))
            self.image = pygame.transform.scale(self.image, bullet_size)
        except:
            # Create a default rectangle if image not found
            self.image = pygame.Surface((3, 7))
            self.image.fill((255, 0, 0))  # Red color
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 5
    
    def update(self):
        self.rect.y += self.speed

class EnemyManager:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        
        # Create rectangular formation of enemies
        self.create_enemy_formation()
    
    def create_enemy_formation(self):
        # Define grid parameters
        rows = 4
        cols = 8
        enemy_width = 40  # Same as enemy size defined in Enemy class
        enemy_height = 40
        horizontal_spacing = 20  # Space between enemies horizontally
        vertical_spacing = 20    # Space between enemies vertically
        
        # Calculate total width of formation
        formation_width = cols * (enemy_width + horizontal_spacing) - horizontal_spacing
        
        # Calculate starting x position to center the formation
        start_x = (self.screen_width - formation_width) // 2
        start_y = 50  # Starting y position from top
        
        # Create enemies in grid formation
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (enemy_width + horizontal_spacing)
                y = start_y + row * (enemy_height + vertical_spacing)
                enemy = Enemy(x, y)
                self.enemy_group.add(enemy)
    
    def update(self):
        # Handle enemy shooting
        for enemy in self.enemy_group:
            if enemy.can_shoot():
                bullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom)
                self.bullet_group.add(bullet)
        
        # Update enemy positions (no movement in new implementation)
        self.enemy_group.update()
        
        # Update bullet positions
        self.bullet_group.update()
        
        # Remove off-screen bullets
        for bullet in self.bullet_group.copy():
            if bullet.rect.top > pygame.display.get_surface().get_height():
                self.bullet_group.remove(bullet)