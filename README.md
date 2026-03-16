# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose**: A number guessing game built with Streamlit where players pick a difficulty level and try to guess a secret number within a limited number of attempts. The game provides hints (Too High / Too Low) and tracks a running score.

**Bugs found**:
1. **Swapped hints** — `check_guess` returned "Too High" with message "Go HIGHER!" and "Too Low" with "Go LOWER!" — the directions were completely backwards.
2. **Wrong Hard mode range** — `get_range_for_difficulty("Hard")` returned `(1, 50)`, which is narrower than Normal, not wider as intended.
3. **Type inconsistency on even attempts** — `app.py` converted the secret number to a string on every even attempt, causing unpredictable comparison results in `check_guess`.
4. **Hardcoded range in UI text** — The info message always displayed "1 and 100" regardless of selected difficulty.
5. **New Game button ignored difficulty** — It always called `random.randint(1, 100)` instead of using the current difficulty range.

**Fixes applied**:
- Implemented all 4 logic functions in `logic_utils.py` with correct behavior.
- Fixed `check_guess` hint directions: "Too High" now says "Go LOWER!", "Too Low" says "Go HIGHER!".
- Fixed Hard difficulty range to `(1, 200)`.
- Updated `app.py` to import from `logic_utils.py` and removed duplicate function definitions.
- Replaced hardcoded range display and New Game button with dynamic `low`/`high` values from the difficulty function.
- Removed the string-conversion bug — `check_guess` always receives integer arguments.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
