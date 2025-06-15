import pygame
import math

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wise Choose Game")

# Load assets
background_image = pygame.image.load('C:/Users/Ashutosh/Documents/Choose Wise/assets/images/background.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

win_sound = pygame.mixer.Sound("C:/Users/Ashutosh/Documents/Choose Wise/assets/sound/win.wav")
pygame.mixer.music.load("C:/Users/Ashutosh/Documents/Choose Wise/assets/sound/background_music.mp3")
pygame.mixer.music.play(-1)

# Game variables
font = pygame.font.Font(None, 36)
players = []
player_scores = {}
player_guesses = {}
current_player_index = 0
round_number = 1
winning_number = 0
eliminated_players = []
round_in_progress = False
show_rules = True
show_results = False
round_winner = None
adding_players = True

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 223, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Function to display text
def draw_text(text, size, color, x, y, center=False):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    if center:
        rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, rect)
    else:
        screen.blit(text_surface, (x, y))

# Calculate the winning number and determine round results
def calculate_winner():
    global winning_number, round_in_progress, round_winner, show_results

    guesses = list(player_guesses.values())
    winning_number = round(sum(guesses) / len(guesses) * 0.8)

    # Identify players who guessed the winning number
    winners = [player for player, guess in player_guesses.items() if guess == winning_number]

    if len(winners) > 1:
        for winner in winners:
            player_scores[winner] -= 1  # Apply penalty for multiple winners
        round_winner = "Multiple Winners"
    elif winners:
        round_winner = winners[0]
        player_scores[round_winner] += 1
    else:
        # Award the closest guess if no exact match
        closest_player = min(player_guesses, key=lambda p: abs(player_guesses[p] - winning_number))
        round_winner = closest_player
        player_scores[closest_player] += 1

    # Deduct points for others
    for player in player_scores:
        if player != round_winner and player not in winners:
            player_scores[player] -= 1

    # Eliminate players with scores <= -5
    for player in list(player_scores.keys()):
        if player_scores[player] <= -5:
            eliminated_players.append(player)
            players.remove(player)
            del player_scores[player]
            del player_guesses[player]

    round_in_progress = False
    show_results = True
    win_sound.play()

# Display the rules
def display_rules():
    screen.fill(BLACK)
    draw_text("GAME RULES:", 48, GOLD, SCREEN_WIDTH // 2, 50, center=True)
    rules = [
        "1. Each player guesses a number.",
        "2. The winning number is 80% of the average of all guesses.",
        "3. Closest guess earns +1 point; others lose -1 point.",
        "4. Multiple winners lose -1 point.",
        "5. Eliminate players with scores of -5.",
        "6. The last player standing wins!"
    ]
    y_offset = 100
    for rule in rules:
        draw_text(rule, 36, WHITE, SCREEN_WIDTH // 2, y_offset, center=True)
        y_offset += 50
    draw_text("Press SPACE to start the game.", 36, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, center=True)
    pygame.display.flip()

# Display round results
def display_results():
    screen.fill(BLACK)
    draw_text(f"Winning Number: {winning_number}", 48, GOLD, SCREEN_WIDTH // 2, 30, center=True)
    draw_text("Player Guesses and Scores:", 36, WHITE, SCREEN_WIDTH // 2, 80, center=True)

    y_offset = 120
    for player, guess in player_guesses.items():
        score = player_scores[player]
        color = GREEN if guess == winning_number else RED
        penalty_text = " (Penalty -1)" if len([p for p, g in player_guesses.items() if g == winning_number]) > 1 else ""
        draw_text(f"{player}: Guess = {guess}, Score = {score}{penalty_text}", 36, color, SCREEN_WIDTH // 2, y_offset, center=True)
        y_offset += 40

    draw_text(f"Round Winner: {round_winner}", 36, GOLD, SCREEN_WIDTH // 2, y_offset + 20, center=True)
    draw_text("Press any key to start the next round.", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, center=True)
    pygame.display.flip()

# Game loop
running = True
user_input = ""
while running:
    screen.blit(background_image, (0, 0))
    if adding_players:
        draw_text(f"Enter Player {len(players) + 1}'s Name:", 36, WHITE, SCREEN_WIDTH // 2, 50, center=True)
        draw_text(user_input, 36, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
    elif show_rules:
        display_rules()
    elif round_in_progress:
        draw_text(f"Round: {round_number}", 48, WHITE, SCREEN_WIDTH // 2, 30, center=True)
        draw_text(f"{players[current_player_index]}'s Turn - Enter your number:", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
        hidden_input = '*' * len(user_input) if user_input else ""
        draw_text(hidden_input, 36, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
    elif show_results:
        display_results()
    else:
        round_number += 1
        player_guesses = {player: None for player in players}
        current_player_index = 0
        round_in_progress = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if adding_players:
                if event.key == pygame.K_RETURN:
                    if user_input.strip():
                        players.append(user_input.strip())
                        player_scores[user_input.strip()] = 0
                        user_input = ""
                        if len(players) == 4:
                            adding_players = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isalnum() and len(user_input) < 20:
                    user_input += event.unicode
            elif show_rules and event.key == pygame.K_SPACE:
                show_rules = False
                round_in_progress = True
            elif round_in_progress:
                if event.key == pygame.K_RETURN and user_input.isdigit():
                    player_guesses[players[current_player_index]] = int(user_input)
                    user_input = ""
                    current_player_index += 1
                    if current_player_index == len(players):
                        calculate_winner()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isdigit() and len(user_input) < 3:
                    user_input += event.unicode
            elif show_results:
                show_results = False

    pygame.display.flip()

pygame.quit()
