import pygame, random, os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HIGHSCORE_PATH = os.path.join(BASE_DIR, "highscore.txt")

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(BASE_DIR, "assets", "METAL_BOSS.wav"))
pygame.mixer.music.set_volume(0.4)

def load_highscore():
    try:
        with open(HIGHSCORE_PATH, "r") as f:
            return int(f.read().strip() or 0)
    except (FileNotFoundError, ValueError):
        return 0

def save_highscore(value):
    with open(HIGHSCORE_PATH, "w") as f:
        f.write(str(int(value)))

'''
Welcome to PA0 – Flappy Bird! Throughout this code, you are going to find a recreation of a game you have probably
heard of before. This is an introductory assignment designed to help you familiarize yourself with what you can expect 
in future PAs. In this PA, you will barely need to code—mostly just tweaking some variable values and implementing
fewer than five lines of new code. It is recommended that you read through the code and the comments explaining 
some of the game mechanics.
'''
# Setup the screen -->
screen = pygame.display.set_mode((400, 600))
BG_PATH = os.path.join(BASE_DIR, "assets", "background.png")
bg_img = pygame.image.load(BG_PATH).convert()
bg_img = pygame.transform.scale(bg_img, (400, 600))
BG_SPIKE_PATH  = os.path.join(BASE_DIR, "assets", "inverted_image.png")
bg_spike  = pygame.image.load(BG_SPIKE_PATH).convert()
bg_spike  = pygame.transform.scale(bg_spike, (400, 600))

pygame.display.set_caption("Flappy Bird")
score_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "score.wav"))
# Colors -->
# NOTE: This is in the RGB (Red, Green, Blue) format
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PLAYER = RED

# Font Size -->
big_font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 30)

# Text Coordinates -->
title_x = 50
title_y = 150

instruction_x = 80
instruction_y = 550

score_x = 200
score_y = 10
high_score = load_highscore()

# Player Variables -->
bird_x = 50
bird_y = 300
bird_velocity = 0
# TODO 1: Tweaking the physics
# Looks like the player is falling too quickly not giving a change to flap it's wing, maybe tweak around with the value of this variable
gravity = 0.5
jump = -8
# Pipe Variables -->
pipe_x = 400
pipe_width = 70
# TODO 2.1: A Little gap Problem
# You probably noticed when running the code that it's impossible the player to go through the gaps
# play around with the pipe_gap variable so that its big enough for the player to pass through
pipe_gap = 150
pipe_height = random.randint(80, 600 - pipe_gap - 80)
# TODO 2.2: The too fast problem
# The pipes are moving way too fast! Play around with the pipe_speed variable until you find a good
# speed for the player to play in!
pipe_speed = 4

score = 0
game_over = False
game_started = False
scored = False
pipe_color = GREEN
start_time_ms = None
difficulty_spiked = False

base_pipe_speed = pipe_speed
base_pipe_gap = pipe_gap
base_gravity = gravity

clock = pygame.time.Clock()

running = True
while running:
    # TODO 6: Changing the name!
    # Doh! This is not out name isn't follow the detailed instructions on the PDF to complete this task.
    player_name = "Jericho"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                    bird_velocity = jump
                    pygame.mixer.music.play(-1)
                    start_time_ms = pygame.time.get_ticks()
                    difficulty_spiked = False
                elif not game_over:
                    bird_velocity = jump
                else:
                    # TODO 3: Spawning back the Player
                    # After the bird crashes with a pipe the when spawning back the player it doesn't appear.
                    # It is your job to find why this is happening! (Hint: What variable stores the y coordinates
                    # of the bird)
                    bird_velocity = 0
                    pipe_x = 400
                    bird_y = 300
                    score = 0
                    game_over = False
                    game_started = True
                    scored = False
                    pygame.mixer.music.stop()
                    pygame.mixer.music.play(-1)
                    start_time_ms = pygame.time.get_ticks()
                    difficulty_spiked = False
                    BLACK = (0, 0, 0)
                    PLAYER = RED
                    pipe_speed = base_pipe_speed
                    pipe_gap = base_pipe_gap
                    gravity = base_gravity
                    pipe_color = GREEN
                    pipe_height = random.randint(80, 600 - pipe_gap - 80)
    if game_started and not game_over:
        bird_velocity += gravity
        bird_y += bird_velocity
        pipe_x -= pipe_speed
        if start_time_ms is not None:
            elapsed = pygame.time.get_ticks() - start_time_ms
            if not difficulty_spiked and elapsed >= 16000:
                pipe_speed = base_pipe_speed + 3
                pipe_gap = max(110, base_pipe_gap - 25)
                gravity = base_gravity + 0.15
                difficulty_spiked = True
                pipe_color = RED
                BLACK = WHITE
                PLAYER = GREEN
        if not scored and (pipe_x + pipe_width) < bird_x:
            score += 1
            score_sound.play()
            scored = True

            if score > high_score:
                high_score = score
                save_highscore(high_score)

        if pipe_x < -70:
            pipe_x = 400
            pipe_height = random.randint(80, 600 - pipe_gap - 80)
            scored = False

        if bird_y > 600 or bird_y < 0:
            game_over = True
            pygame.mixer.music.stop()
        bird_rect = pygame.Rect(bird_x, bird_y, 30, 30)
        top_pipe_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        bottom_pipe_rect = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, 600)

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            game_over = True
            pygame.mixer.music.stop()

    screen.blit(bg_spike if difficulty_spiked else bg_img, (0, 0))
    # TODO 5: A Bird's Color
    # The color of the player is currently white, let's change that a bit! You are free to change the bird's
    # to whatever you wish. You will need to head back to where the PLAYER variable was created and change the values.
    pygame.draw.rect(screen, PLAYER, (bird_x, bird_y, 30, 30)) # Drawing the bird (You don't need to touch this line!)
    pygame.draw.rect(screen, pipe_color, (pipe_x, 0, pipe_width, pipe_height))
    pygame.draw.rect(screen, pipe_color, (pipe_x, pipe_height + pipe_gap, pipe_width, 600))

    if not game_started: # Start UI -->
        title_text = big_font.render("Flappy Bird", True, BLACK)
        instruction_text = small_font.render("Press space bar to flap!", True, BLACK)
        screen.blit(title_text, (title_x, title_y))
        screen.blit(instruction_text, (instruction_x, instruction_y))

    if game_over: # GameOver UI -->
        loss_text = small_font.render("Press Space to restart...", True, BLACK)
        screen.blit(loss_text, (85, 200))

    score_text = small_font.render(str(score), True, BLACK)
    screen.blit(score_text, (score_x, score_y))
    hs_text = small_font.render(f"HS: {high_score}", True, BLACK)
    screen.blit(hs_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()