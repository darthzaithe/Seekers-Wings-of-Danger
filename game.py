import pygame
import sys
import math
import random
import config
import menu
import state

### Config imports ###
screen_width = config.SCREEN_WIDTH
screen_height = config.SCREEN_HEIGHT
framerate_cap = config.FRAMERATE_CAP

menu_color = {
    "selected": config.MENU_COLOR_SELECTED,
    "unselected": config.MENU_COLOR_UNSELECTED
}

def run_game():
    
    game_state = state.GameState(screen_width, screen_height)

    # Enemy
    enemy_size = 40
    enemy_color = config.ENEMY_COLOR

    def spawn_enemy(enemy_size, screen_width):
        enemy_x = random.randint(0, game_state.screen_width - enemy_size)
        enemy_y = 50
        return pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)

    game_state.enemy_rect = spawn_enemy(enemy_size, game_state.screen_width)

    screen = pygame.display.set_mode((game_state.screen_width, game_state.screen_height))
    pygame.display.set_caption("Seekers")
    clock = pygame.time.Clock()

    # Set up fonts
    title_font = pygame.font.Font(None, 56)
    menu_font = pygame.font.Font(None, 32)

    # Menus
    main_menu_items = ["New Game", "Settings"]
    character_menu_items = ["Starscream", "Thundercracker", "Skywarp"]

    # Colors and fonts
    fonts = (title_font, menu_font)
    colors = (menu_color["selected"], menu_color["unselected"])

    # Sprite
    starscream_sprite = pygame.image.load("sprites/characters/screamer.png").convert_alpha()
    thundercracker_sprite = pygame.image.load("sprites/characters/cracker.png").convert_alpha()
    skywarp_sprite = pygame.image.load("sprites/characters/warp.png").convert_alpha()

    character_sprites = {
        "Starscream": starscream_sprite,
        "Thundercracker": thundercracker_sprite,
        "Skywarp": skywarp_sprite
    }

    current_player_sprite = None
    player_speed = 5

    # Score
    score_font = pygame.font.Font(None, 32)

    # Projectile
    projectile_speed = -10
    particle_color = config.PROJECTILE_COLOR

    # Main loop
    running = True
    time_counter = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state.current_screen == "main_menu":
                game_state.selected_menu_index = menu.handle_menu_input(event, game_state.selected_menu_index, len(main_menu_items))
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    selected_item = main_menu_items[game_state.selected_menu_index]
                    if selected_item == "New Game":
                        game_state.current_screen = "character_select"
                        game_state.selected_menu_index = 0
                    else:
                        print(f"Selected: {selected_item}")

            elif game_state.current_screen == "character_select":
                game_state.selected_menu_index = menu.handle_menu_input(event, game_state.selected_menu_index, len(character_menu_items))
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    game_state.chosen_character = character_menu_items[game_state.selected_menu_index]

                    if game_state.chosen_character == "Starscream":
                        current_player_sprite = starscream_sprite
                    elif game_state.chosen_character == "Thundercracker":
                        current_player_sprite = thundercracker_sprite
                    elif game_state.chosen_character == "Skywarp":
                        current_player_sprite = skywarp_sprite

                    game_state.player_rect = current_player_sprite.get_rect(center=(screen_width // 2, screen_height // 2))

                    game_state.current_screen = "game"

            elif game_state.current_screen == "game":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    particle_x = game_state.player_rect .centerx
                    particle_y = game_state.player_rect .top
                    game_state.projectiles.append({'pos': [particle_x, particle_y], 'speed': [0, projectile_speed]})

        keys = pygame.key.get_pressed()
        if game_state.current_screen == "game" and game_state.player_rect :
            if keys[pygame.K_w]:
                game_state.player_rect .y -= player_speed
            if keys[pygame.K_s]:
                game_state.player_rect .y += player_speed
            if keys[pygame.K_a]:
                game_state.player_rect .x -= player_speed
            if keys[pygame.K_d]:
                game_state.player_rect .x += player_speed

            game_state.player_rect .clamp_ip(screen.get_rect())

        # Title pulse
        time_counter += 0.075
        title_brightness = 190 + int(75 * math.sin(time_counter))
        title_brightness = max(0, min(255, title_brightness))
        title_color = (title_brightness, title_brightness, title_brightness)

        # Background fill
        screen.fill((30, 30, 30))

        # Draw current screen
        if game_state.current_screen == "main_menu":
            menu.draw_menu(
                screen, 
                "Seekers: Wings of Danger", 
                main_menu_items, 
                game_state.selected_menu_index, 
                fonts, 
                colors, 
                screen_width, 
                screen_height, 
                title_color
            )

        elif game_state.current_screen == "character_select":
            menu.draw_menu(
                screen, 
                "Select your character", 
                character_menu_items, 
                game_state.selected_menu_index, 
                fonts, 
                colors, 
                screen_width, 
                screen_height, 
                title_color,
                character_sprites,
                character_menu_items[game_state.selected_menu_index]
            )

        elif game_state.current_screen == "game":
            screen.blit(current_player_sprite, game_state.player_rect )

            score_surface = score_font.render(f"Score: {game_state.score}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(topright=(screen_width - 10, 10))
            screen.blit(score_surface, score_rect)
        
            if game_state.enemy_active and game_state.enemy_rect:
                pygame.draw.rect(screen, enemy_color, game_state.enemy_rect)
                game_state.enemy_rect.y += game_state.enemy_speed

                if game_state.enemy_rect.top > screen_height:
                    game_state.game_state.enemy_rect = spawn_enemy()


            # Collision detection enemy/player

            if game_state.enemy_active and game_state.player_rect.colliderect(game_state.enemy_rect):
                game_state.current_screen = "game_over"
                game_over_time = pygame.time.get_ticks()

            for particle in game_state.projectiles:
                pygame.draw.circle(screen, particle_color, (int(particle['pos'][0]), int(particle['pos'][1])), 5)

                particle['pos'][0] += particle['speed'][0]
                particle['pos'][1] += particle['speed'][1]

                # Collision detection particle/enemy
                if game_state.enemy_active and game_state.enemy_rect.collidepoint(particle['pos']):
                    game_state.enemy_active = False
                    game_state.projectiles.remove(particle)
                    game_state.score += 100

                    if game_state.score % 1000 == 0:
                        game_state.enemy_speed += 1

                    # Respawn
                    game_state.enemy_rect = spawn_enemy(enemy_size, game_state.screen_width)
                    game_state.enemy_active = True

            projectile = [p for p in game_state.projectiles if p['pos'][1] > 0]

        elif game_state.current_screen == "game_over":
            screen.fill((30, 30, 30))
            game_over_surface = title_font.render("GAME OVER", True, (255, 0, 0))
            score_surface = menu_font.render(f"Final Score: {game_state.score}", True, (255, 255, 255))
            game_over_rect = game_over_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
            score_rect = score_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
            screen.blit(game_over_surface, game_over_rect)
            screen.blit(score_surface, score_rect)

            if pygame.time.get_ticks() - game_over_time >= 10000:
                game_state.reset()
                game_state.enemy_rect = spawn_enemy(enemy_size, game_state.screen_width)
                
        # Update display
        pygame.display.flip()
        clock.tick(framerate_cap)

    pygame.quit()
    sys.exit()
