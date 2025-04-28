import random
import time
import pygame  # 🎶 For music and sounds

# Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

# Symbol settings
symbols_count = {
    "🍒": 2,  # Cherry
    "🍋": 4,  # Lemon
    "🔔": 6,  # Bell
    "🍀": 8,  # Clover
    "💎": 10,  # Diamond
}

symbols_value = {
    "🍒": 5,
    "🍋": 4,
    "🔔": 3,
    "🍀": 2,
    "💎": 1,
}

# Initialize pygame mixer
pygame.mixer.init()

# Load sounds
background_music = "background_music.mp3"
spin_sound = "spin.wav"
win_sound = "win.wav"


# Start background music
def start_background_music():
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)  # -1 means loop forever


# Play spin sound
def play_spin_sound():
    spin = pygame.mixer.Sound(spin_sound)
    spin.play()


# Play win sound
def play_win_sound():
    win = pygame.mixer.Sound(win_sound)
    win.play()


def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")


def rules():
    print_colored("\n🎰 Welcome to the Slot Machine! 🎰", "1;34")
    print(
        """
📜 Rules:
- Match symbols across a line to WIN.
- Some symbols are rarer and more valuable.
- Jackpot if all rows match the same symbol! 🎉
- Bet wisely and have fun! 🍀
    """
    )


def calculate_winnings(columns, lines, bet, value):
    winnings = 0
    winning_lines = []
    jackpot = False

    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            win = value[symbol] * bet
            winnings += win
            winning_lines.append(line + 1)

    # Jackpot check (all symbols same across all slots)
    flattened = [symbol for col in columns for symbol in col]
    if all(s == flattened[0] for s in flattened):
        print_colored("🎉 JACKPOT!! 🎉", "1;33")
        winnings += 50 * bet  # Jackpot bonus

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)

    return columns


def spin_animation():
    print("\nSpinning...", end="")
    play_spin_sound()  # << added here!
    for _ in range(5):
        print(" 🌀", end="", flush=True)
        time.sleep(0.4)
    print("\n")


def print_slot_machine(columns):
    print_colored("\n🎰 Slot Machine 🎰", "1;35")
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()
    print()


def deposit():
    while True:
        amount = input("💰 Enter the amount to deposit: $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                print(f"✅ Deposited: ${amount}\n")
                break
            else:
                print("⚠️ Amount must be greater than 0.")
        else:
            print("❌ Invalid input. Please enter a number.")
    return amount


def get_number_of_lines():
    while True:
        lines = input(f"🎯 Enter the number of lines to bet on (1-{MAX_LINES}): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                print(f"✅ Number of lines: {lines}")
                break
            else:
                print(f"⚠️ Lines must be between 1 and {MAX_LINES}.")
        else:
            print("❌ Invalid input.")
    return lines


def get_bet():
    while True:
        bet = input("💵 Enter the bet amount for each line: $")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                print(f"✅ Bet amount: ${bet}")
                break
            else:
                print(f"⚠️ Bet must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("❌ Invalid input.")
    return bet


def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(
                f"⚠️ Your total bet of ${total_bet} exceeds your balance of ${balance}."
            )
            continue
        else:
            break

    print(f"🎲 Betting ${bet} on {lines} line(s). Total bet: ${total_bet}.\n")

    spin_animation()
    slots = get_slot_machine_spin(ROWS, COLS, symbols_count)
    print_slot_machine(slots)

    winnings, winning_lines = calculate_winnings(slots, lines, bet, symbols_value)
    print_colored(f"🏆 You won ${winnings}!", "1;32")
    if winnings > 0:
        play_win_sound()  # << play when there's a win!

    if winning_lines:
        print(f"🎯 Winning line(s):", *winning_lines)
    else:
        print("💔 No winning lines.")

    return winnings - total_bet


def main():
    start_background_music()
    print_colored("🎉 Welcome to the Ultimate Slot Machine 🎉", "1;36")
    while True:
        view_rules = input("📜 View rules? (y/n): ").lower()
        if view_rules == "y":
            rules()
            break
        elif view_rules == "n":
            break
        else:
            print("❌ Invalid input.")

    balance = deposit()
    while True:
        print_colored(f"\n💰 Current balance: ${balance}", "1;34")
        answer = input(
            "Press 's' to spin 🎰, 'r' for rules 📜, or 'q' to quit ❌: "
        ).lower()
        if answer == "s":
            balance += spin(balance)
        elif answer == "r":
            rules()
        elif answer == "q":
            print_colored("\n👋 Thanks for playing! Goodbye!", "1;36")
            break
        else:
            print("❌ Invalid input. Please enter 's', 'r', or 'q'.")

        if balance <= 0:
            print_colored("\n💔 You have run out of money!", "1;31")
            break

    print_colored(f"\n🏁 Final balance: ${balance}", "1;33")


if __name__ == "__main__":
    main()
