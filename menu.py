import pygame

def draw_menu(screen, title, items, selected_index, fonts, colors, screen_width, screen_height, title_color, character_sprites=None, highlighted_item = None):
    title_font, item_font = fonts
    selected_color, unselected_color = colors

    # Draw title
    title_surface = title_font.render(title, True, title_color)
    title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(title_surface, title_rect)

    # Menu items
    max_width = max(item_font.render(item, True, (0, 0, 0)).get_width() for item in items)
    buffer_space = 300
    left_x = (screen_width - max_width) // 2 + buffer_space

    if character_sprites and highlighted_item:
        preview_sprite = character_sprites[highlighted_item]
        sprite_scaled = pygame.transform.scale(preview_sprite, (200, 200)) 

        sprite_x = screen_width // 4 - sprite_scaled.get_width() // 2

        menu_top_y = screen_height // 2 + 50
        menu_bottom_y = menu_top_y + (len(items) - 1) * 50
        menu_center_y = (menu_top_y + menu_bottom_y) // 2

        sprite_y = menu_center_y - sprite_scaled.get_height() // 2

        screen.blit(sprite_scaled, (sprite_x, sprite_y))

    for i, item in enumerate(items):
        base_color = (255, 255, 255)

        if i == selected_index:
            color = base_color
        else:
            color = tuple(int(c * 0.6) for c in base_color)

        item_surface = item_font.render(item, True, color)
        item_rect = item_surface.get_rect(topleft=(left_x // 2, screen_height // 2 + (i + 1) * 50))
        screen.blit(item_surface, item_rect)

def handle_menu_input(event, selected_index, item_count):
    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_UP, pygame.K_w]:
            selected_index = (selected_index - 1) % item_count
        if event.key in [pygame.K_DOWN, pygame.K_s]:
            selected_index = (selected_index + 1) % item_count
    return selected_index