import random
import streamlit as st

# --- Setup the page ---
st.set_page_config(
    page_title="Guess the Number!", 
    page_icon="🎯", 
    layout="wide"
)

# --- Game settings based on difficulty ---
def get_game_settings(difficulty):
    if difficulty == "Easy 😊":
        return {"min": 1, "max": 50, "attempts": 10}
    elif difficulty == "Medium 🤔":
        return {"min": 1, "max": 100, "attempts": 8}
    else:  # Hard mode
        return {"min": 1, "max": 1000, "attempts": 6}

# --- Sidebar with rules ---
with st.sidebar:
    st.title("🎯 Game Rules")
    st.write("Try to guess the secret number!")
    st.write("- You'll get hints after each guess")
    st.write("- Different difficulties change:")
    st.write("  • Number range (Easy:1-50, Medium:1-100, Hard:1-1000)")
    st.write("  • Attempts allowed (Easy:10, Medium:8, Hard:6)")
    st.markdown("---")
    
    # Difficulty selector - this now triggers game reset when changed
    difficulty = st.radio(
        "Select difficulty:",
        ["Easy 😊", "Medium 🤔", "Hard 😈"],
        index=1,  # Default to medium
        key="difficulty_selector",
        on_change=lambda: st.session_state.update({
            "game_settings": get_game_settings(st.session_state.difficulty_selector),
            "secret_number": random.randint(
                get_game_settings(st.session_state.difficulty_selector)["min"],
                get_game_settings(st.session_state.difficulty_selector)["max"]
            ),
            "attempts": 0,
            "game_over": False
        })
    )
    
    st.markdown("---")
    st.write("Made By Syed Muhammad Hussain")

# --- Initialize game state ---
if 'game_settings' not in st.session_state:
    st.session_state.game_settings = get_game_settings(difficulty)
    st.session_state.secret_number = random.randint(
        st.session_state.game_settings["min"],
        st.session_state.game_settings["max"]
    )
    st.session_state.attempts = 0
    st.session_state.game_over = False

# --- Main game area ---
st.title("Guess the Number Game")
st.write(f"Difficulty: **{difficulty}**")
st.write(f"Guess between {st.session_state.game_settings['min']} and {st.session_state.game_settings['max']}")

# The guess input - now properly updates with difficulty
guess = st.number_input(
    "Your guess:",
    min_value=st.session_state.game_settings["min"],
    max_value=st.session_state.game_settings["max"],
    step=1,
    key="guess_input"
)

# Check guess button
if st.button("🔍 Check My Guess", type="primary"):
    if st.session_state.game_over:
        st.warning("Game over! Click 'New Game' to play again.")
    else:
        st.session_state.attempts += 1
        
        if guess < st.session_state.secret_number:
            st.error("Too low! 📉")
        elif guess > st.session_state.secret_number:
            st.error("Too high! 📈")
        else:
            st.success(f"Perfect! 🎉 You got it in {st.session_state.attempts} tries!")
            st.balloons()
            st.session_state.game_over = True
        
        # Check if out of attempts
        max_attempts = st.session_state.game_settings["attempts"]
        if st.session_state.attempts >= max_attempts and not st.session_state.game_over:
            st.error(f"Out of tries! The number was {st.session_state.secret_number}.")
            st.session_state.game_over = True

# Show attempts remaining
if not st.session_state.game_over and st.session_state.attempts > 0:
    remaining = st.session_state.game_settings["attempts"] - st.session_state.attempts
    st.write(f"Attempts: {st.session_state.attempts}/{st.session_state.game_settings['attempts']}")
    if remaining < 3:
        st.warning(f"Only {remaining} guesses left!")

# New game button
if st.button("🔄 New Game", type="secondary"):
    st.session_state.game_settings = get_game_settings(difficulty)
    st.session_state.secret_number = random.randint(
        st.session_state.game_settings["min"],
        st.session_state.game_settings["max"]
    )
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.rerun()