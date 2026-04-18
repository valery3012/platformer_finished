import pygame
from BlockClass import Block
from WindowClass import Window
from CoinsClass import Coin
from RockClass import Rock

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE = 50

window = Window(WIDTH, HEIGHT)
clock = pygame.time.Clock()

# --- ГРАВЕЦЬ ---
player = pygame.Rect(100, 400, 40, 48)
speed = 5
vel_x = 0
vel_y = 0
gravity = 0.5
jump_power = -12
on_ground = False

start_x = 100
start_y = 400

deaths = 0
dead_bodies = []

menu_state = "main"

# --- КАРТИНКИ ---
player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))

dead_img = pygame.transform.rotate(player_img, 90)

block_img = pygame.image.load("block.png").convert_alpha()
block_img = pygame.transform.scale(block_img, (TILE, TILE))

rock_img = pygame.image.load("rock.png").convert_alpha()
rock_img = pygame.transform.scale(rock_img, (TILE, TILE))

coin_img = pygame.image.load("coin.png").convert_alpha()

spike_img = pygame.image.load("spike.png").convert_alpha()
spike_img = pygame.transform.scale(spike_img, (50, 25))

bg = pygame.image.load("background.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

finish_img = pygame.image.load("finish.png").convert_alpha()
finish_img = pygame.transform.scale(finish_img, (70, 70))

menu_panel = pygame.image.load("menu_panel.png").convert_alpha()

button_start = pygame.image.load("button_start.png").convert_alpha()
button_retry = pygame.image.load("button_retry.png").convert_alpha()
button_resume = pygame.image.load("button_resume.png").convert_alpha()
button_how = pygame.image.load("button_howtoplay.png").convert_alpha()
button_quit = pygame.image.load("button_quit.png").convert_alpha()

start_btn = pygame.transform.scale(button_start, (180, 55))
how_btn = pygame.transform.scale(button_how, (180, 55))   # менша
quit_btn = pygame.transform.scale(button_quit, (180, 55))
resume_btn = pygame.transform.scale(button_resume, (180, 55))   # менша
retry_btn = pygame.transform.scale(button_retry, (180, 55))

# --- КАМЕРА ---
scroll_x = 0
MAP_WIDTH = 4000

# --- РІВЕНЬ ---
ground = [(x, 550) for x in range(0, 4000, 50)]

platforms = [
    (300,450),(350,450),(400,450),
    (700,400),(750,400),(800,400),
    (1100,400),(1150,400),(1200,400),
    (1500,420),(1550,420),
    (1800,380),(1850,380),(1900,380),
    (2100,350),

    (2250,300),(2300,300),
    (2500,350),
    (2700,280),
    (2900,320),

    (3200,400),(3250,400),
    (3450,350),
    (3650,300)
]

rocks_pos = [
    (3800,500),(3800,450),(3800,400),
    (3850,500),(3850,450),(3850,400),
    (3850,350),(3850,300),
    (3900,500),(3900,450),(3900,400),
    (3900,350),(3900,300),
    (3950,500),(3950,450),(3950,400),
    (3950,350),(3950,300),
    (3850,250), (3900,250), (3950,250)
]

pillars = [
    (500,500),(500,450),
    (1300,500),(1300,450),(1300,400)
]

boxes = [
    (200,500),(900,500),(1600,500)
]

spikes_pos = [
    (550, 525),
    (950, 525),
    (1250, 525),
    (1450, 525),
    (1750, 525),
    (1850, 355),

    (2100, 525),
    (2350, 525),
    (2600, 525),
    (2800, 525),

    (3100, 525),
    (3400, 525),
    (3700, 525)
]

coins_pos = [
    (310, 400),
    (670, 370),
    (1020, 330),
    (1320, 290),
    (1610, 360),

    (2270, 250),
    (2540, 300),
    (2720, 230),
    (2910, 270),

    (3210, 350),
    (3460, 300),
    (3710, 250)
]

coins = [Coin(x, y, coin_img) for x, y in coins_pos] 

level_blocks = ground + platforms + pillars + boxes
blocks = [Block(x, y, TILE, block_img) for x, y in level_blocks]
spikes = [Block(x, y, TILE, spike_img) for x, y in spikes_pos]
rocks = [Block(x, y, TILE, rock_img) for x, y in rocks_pos]
finish = pygame.Rect(3930, 180, 70, 70)
FINISH_COLOR = (255, 215, 0)

coin_count = 0
font = pygame.font.SysFont("Arial", 30)

# --- ГРА ---

def draw_image_button(screen, image, pos, mouse):
    rect = image.get_rect(topleft=pos)

    if rect.collidepoint(mouse):
        image = pygame.transform.scale(image, (rect.width + 5, rect.height + 5))
        rect = image.get_rect(center=rect.center)

    screen.blit(image, rect.topleft)
    return rect


def draw_menu_background():
    window.screen.blit(bg, (0, 0))

    dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, 160))
    window.screen.blit(dark_overlay, (0, 0))

def pause_menu():
    while True:
        mouse = pygame.mouse.get_pos()

        draw_menu_background()

        panel_rect = menu_panel.get_rect(center=(WIDTH//2, HEIGHT//2))
        window.screen.blit(menu_panel, panel_rect.topleft)

        font = pygame.font.SysFont("Arial", 30)

        resume_rect = draw_image_button(window.screen, resume_btn, (310, 200), mouse)
        retry_rect = draw_image_button(window.screen, retry_btn, (310, 270), mouse)
        quit_rect = draw_image_button(window.screen, quit_btn, (310, 340), mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    return "resume"
                if retry_rect.collidepoint(event.pos):
                    return "retry"
                if quit_rect.collidepoint(event.pos):
                    return "quit"

        window.update()

def start_menu():
    global menu_state

    font = pygame.font.SysFont("Arial", 22)

    while True:
        mouse = pygame.mouse.get_pos()

        draw_menu_background()

        panel_rect = menu_panel.get_rect(center=(WIDTH//2, HEIGHT//2))
        window.screen.blit(menu_panel, panel_rect.topleft)

        # =========================
        # ГОЛОВНЕ МЕНЮ
        # =========================
        if menu_state == "main":

            start_rect = draw_image_button(window.screen, start_btn, (310, 200), mouse)
            how_rect = draw_image_button(window.screen, how_btn, (310, 270), mouse)
            quit_rect = draw_image_button(window.screen, quit_btn, (310, 340), mouse)

        # =========================
        # HOW TO PLAY ЕКРАН
        # =========================
        elif menu_state == "how":

            text_lines = [
                "You are a knight.",
                "Your goal is to get to the cave.",
                "Controls:",
                "A - left",
                "D - right",
                "SPACE - jump",
                "Collect coins by touching them."
            ]

            y = 190
            for line in text_lines:
                txt = font.render(line, True, (255, 255, 255))
                window.screen.blit(txt, (280, y))
                y += 25

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if menu_state == "main":

                    if start_rect.collidepoint(event.pos):
                        return

                    if how_rect.collidepoint(event.pos):
                        menu_state = "how"

                    if quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        exit()

                elif menu_state == "how":
                    # клік повертає назад у меню
                    menu_state = "main"

        window.update()


def end_menu(coins, deaths):
    while True:
        mouse = pygame.mouse.get_pos()

        draw_menu_background()

        panel_rect = menu_panel.get_rect(center=(WIDTH//2, HEIGHT//2))
        window.screen.blit(menu_panel, panel_rect.topleft)

        font = pygame.font.SysFont("Arial", 30)

        info1 = font.render(f"Coins: {coins}", True, (255, 255, 255))
        info2 = font.render(f"Deaths: {deaths}", True, (255, 100, 100))

        window.screen.blit(info1, (320, 180))
        window.screen.blit(info2, (320, 220))

        retry_rect = draw_image_button(window.screen, retry_btn, (310, 270), mouse)
        quit_rect = draw_image_button(window.screen, quit_btn, (310, 340), mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    return "retry"
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        window.update()

run = True
start_menu()
while run:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                result = pause_menu()

                if result == "resume":
                    pass

                elif result == "retry":
                    player.x = start_x
                    player.y = start_y
                    vel_x = 0
                    vel_y = 0
                    coin_count = 0
                    deaths = 0

                    for coin in coins:
                        coin.collected = False

                    dead_bodies.clear()

                elif result == "quit":
                    run = False
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # =========================
    # РУХ ПО X
    # =========================
    vel_x = 0

    if keys[pygame.K_a]:
        vel_x = -speed
    if keys[pygame.K_d]:
        vel_x = speed

    player.x += vel_x

    for block in blocks:
        if player.colliderect(block.rect):
            if vel_x > 0:
                player.right = block.rect.left
            elif vel_x < 0:
                player.left = block.rect.right
    
    for rock in rocks:
        if player.colliderect(block.rect):
            if vel_x > 0:
                player.right = block.rect.left
            elif vel_x < 0:
                player.left = block.rect.right

    # =========================
    # СТРИБОК
    # =========================
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump_power
        on_ground = False

    if player.colliderect(finish):
        result = end_menu(coin_count, deaths)

        if result == "retry":
            player.x = start_x
            player.y = start_y
            vel_x = 0
            vel_y = 0
            coin_count = 0
            deaths = 0

            for coin in coins:
                coin.collected = False

            dead_bodies.clear()

            continue

        else:
            run = False

    # =========================
    # ГРАВІТАЦІЯ
    # =========================
    vel_y += gravity
    player.y += vel_y

    on_ground = False

    for block in blocks:
        if player.colliderect(block.rect):

            if vel_y > 0:
                player.bottom = block.rect.top
                vel_y = 0
                on_ground = True

            elif vel_y < 0:
                player.top = block.rect.bottom
                vel_y = 0

    for rock in rocks:
        if player.colliderect(rock.rect):

            if vel_y > 0:
                player.bottom = rock.rect.top
                vel_y = 0
                on_ground = True

            elif vel_y < 0:
                player.top = rock.rect.bottom
                vel_y = 0

    for coin in coins:
        if not coin.collected and player.colliderect(coin.rect):
            coin.collected = True
            coin_count += 1

    for spike in spikes:
        danger_zone = spike.rect.inflate(-10, 0)
        if player.colliderect(danger_zone):

            # створюємо труп
            dead_bodies.append((player.x, player.y + 30))

            # додаємо смерть
            deaths += 1

            # респавн
            player.x = start_x
            player.y = start_y
            vel_x = 0
            vel_y = 0

    # =========================
    # КАМЕРА
    # =========================
    scroll_x = player.x - WIDTH // 2

    if scroll_x < 0:
        scroll_x = 0
    if scroll_x > MAP_WIDTH - WIDTH:
        scroll_x = MAP_WIDTH - WIDTH

    # =========================
    # МАЛЮВАННЯ
    # =========================
    window.screen.blit(bg, (0, 0))

    for body in dead_bodies:
        window.screen.blit(dead_img, (body[0] - scroll_x, body[1]))
    
    for block in blocks:
        block.draw(window.screen, scroll_x)
    
    for rock in rocks:
        rock.draw(window.screen, scroll_x)

    for coin in coins:
        coin.draw(window.screen, scroll_x)

    for spike in spikes:
        spike.draw(window.screen, scroll_x)

    window.screen.blit(finish_img, (finish.x - scroll_x, finish.y))

    window.screen.blit(player_img, (player.x - 5 - scroll_x, player.y))

    text = font.render(f"Coins: {coin_count}", True, (255, 255, 255))
    window.screen.blit(text, (20, 20))

    death_text = font.render(f"Deaths: {deaths}", True, (255, 100, 100))
    window.screen.blit(death_text, (20, 60))

    window.update()

pygame.quit()