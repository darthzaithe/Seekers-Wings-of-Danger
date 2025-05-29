import pygame
import os
import sys
import math
import menu
import random

# Window size
screen_width = 800
screen_height = 600

# Framerate
framerate_cap = 60

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Set up window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Seekers")

# Set up fonts
title_font = pygame.font.Font(None, 56)
menu_font = pygame.font.Font(None, 32)

# Menus
title_string = "Seekers: Wings of Danger"
main_menu_items = ["New Game", "Load Game", "Settings"]
character_menu_items = ["Starscream", "Thundercracker", "Skywarp"]

# State
# States can be "main menu", "character select", "game"
current_screen = "main_menu"
selected_menu_index = 0
chosen_character = None

# Colors and fonts
menu_color = {
    "selected": (255, 255, 255),
    "unselected": (100, 100, 100),
}
fonts = (title_font, menu_font)
colors = (menu_color["selected"], menu_color["unselected"])

# Character colors
character_colors = {
    "Starscream": (225, 0, 0),        
    "Thundercracker": (0, 135, 235),  
    "Skywarp": (150, 0, 150)          
}

# Sprite
sprite_path = os.path.join("sprites", "characters", "screamer.png")
sprite_image = pygame.image.load(sprite_path).convert_alpha()
sprite_rect = sprite_image.get_rect(center=(screen_width // 2, screen_height //2))
sprite_speed = 5

# Enemey
enemy_size = 40
enemy_color = (200, 50, 50)

def spawn_enemy():
    enemy_x = random.randint(0, screen_width - enemy_size)
    enemy_y = 50
    return pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)

enemy_rect = spawn_enemy()
enemy_active = True

# Particle (temp projectile)
particles = []
particle_speed = -10
particle_color = (255, 255, 0)

# Main loop
running = True
time_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == "main_menu":
            selected_menu_index = menu.handle_menu_input(event, selected_menu_index, len(main_menu_items))
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                selected_item = main_menu_items[selected_menu_index]
                if selected_item == "New Game":
                    current_screen = "character_select"
                    selected_menu_index = 0
                else:
                    print(f"Selected: {selected_item}")

        elif current_screen == "character_select":
            selected_menu_index = menu.handle_menu_input(event, selected_menu_index, len(character_menu_items))
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                chosen_character = character_menu_items[selected_menu_index]
                current_screen = "game"

        elif current_screen == "game":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                particle_x = sprite_rect.centerx
                particle_y = sprite_rect.top
                particles.append({'pos': [particle_x, particle_y], 'speed': [0, particle_speed]})

    keys = pygame.key.get_pressed()
    if current_screen == "game":
        if keys[pygame.K_w]:
            sprite_rect.y -= sprite_speed
        if keys[pygame.K_s]:
            sprite_rect.y += sprite_speed
        if keys[pygame.K_a]:
            sprite_rect.x -= sprite_speed
        if keys[pygame.K_d]:
            sprite_rect.x += sprite_speed

        sprite_rect.clamp_ip(screen.get_rect())

    # Title pulse
    time_counter += 0.075
    title_brightness = 190 + int(75 * math.sin(time_counter))
    title_brightness = max(0, min(255, title_brightness))
    title_color = (title_brightness, title_brightness, title_brightness)

    # Background fill
    screen.fill((30, 30, 30))

    # Draw current screen
    if current_screen == "main_menu":
        menu.draw_menu(screen, title_string, main_menu_items, selected_menu_index, fonts, colors, screen_width, screen_height, title_color)
    elif current_screen == "character_select":
        menu.draw_menu(screen, "Select your character", character_menu_items, selected_menu_index, fonts, colors, screen_width, screen_height, title_color)
    elif current_screen == "game":
        screen.blit(sprite_image, sprite_rect)
    
        if enemy_active and enemy_rect:
            pygame.draw.rect(screen, enemy_color, enemy_rect)

        for particle in particles:
            pygame.draw.circle(screen, particle_color, (int(particle['pos'][0]), int(particle['pos'][1])), 5)

            particle['pos'][0] += particle['speed'][0]
            particle['pos'][1] += particle['speed'][1]

            # Colission detection
            if enemy_active and enemy_rect.collidepoint(particle['pos']):
                enemy_active = False
                particles.remove(particle)

                # Respawn
                enemy_rect = spawn_enemy()
                enemy_active = True

        particles = [p for p in particles if p['pos'][1] > 0]

    # Update display
    pygame.display.flip()
    clock.tick(framerate_cap)

pygame.quit()
sys.exit()


