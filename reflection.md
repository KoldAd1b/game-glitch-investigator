# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it appeared to work on the surface but quickly broke down in noticeable ways. The most obvious problem was that the hints were backwards — when I guessed a number that was too high, the game told me to go higher, which made it impossible to converge on the secret number. The Hard difficulty mode also felt identical to Normal because it was secretly using the same range (1–50, not a wider range as expected). Additionally, on every other guess attempt, the game internally converted the secret number to a string before comparing it, causing unpredictable comparison behavior that made certain guesses appear to win or lose incorrectly. Finally, the New Game button always reset the secret to a number between 1 and 100 regardless of the selected difficulty, so switching to Easy didn't actually constrain the range as expected.

Concrete bugs noticed at the start:
- **Hints were reversed**: guessing 80 on a secret of 50 showed "Go HIGHER!" instead of "Go LOWER!"
- **Hard mode range was wrong**: `get_range_for_difficulty("Hard")` returned `(1, 50)` — narrower than Normal, not wider
- **Type inconsistency on even attempts**: `secret` was cast to a string, making `check_guess` unreliable every other turn

---

## 2. How did you use AI as a teammate?

I used Claude Code (via the Claude CLI) as my primary AI tool throughout this project. Claude helped me explore the codebase quickly by reading all relevant files and identifying all six bugs in one pass, which would have taken me much longer to find manually.

**Correct AI suggestion**: Claude correctly identified that the hint messages in `check_guess` were swapped — `"Too High"` was paired with `"📈 Go HIGHER!"` when it should say `"📉 Go LOWER!"`. I verified this by adding a targeted pytest test (`test_hint_direction_too_high`) that checks whether the message string contains "LOWER" when the guess exceeds the secret, and the test passed after applying the fix.

**Incorrect/misleading AI suggestion**: During early exploration, the AI initially suggested that `update_score` might also be buggy because it awards +5 points for "Too High" on even attempts while penalizing "Too Low" consistently. This looked suspicious, but after re-reading the project description and the task instructions, it became clear this asymmetry was intentional design (the game is meant to have "quirky" scoring). I verified by re-reading `tasks.md`, which does not list scoring as a bug to fix, so I left it as-is. This was a case where the AI was pattern-matching on "looks weird" rather than confirmed broken behavior.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed when both a targeted pytest test passed **and** the live Streamlit app behaved correctly on that scenario. Using only one verification method wasn't enough — for example, the type-inconsistency bug was invisible in normal play but clearly showed up when I added the `test_hint_direction_too_high` test and ran it against the original code. After implementing all fixes in `logic_utils.py` and updating `app.py` to import from it, I ran `pytest tests/ -v` and all six tests passed (three original tests updated for the tuple return type, plus three new tests).

For manual verification, I ran `streamlit run app.py`, opened the Developer Debug Info panel to see the secret number, and played through all three difficulty modes to confirm: Hard mode now uses a range of 1–200, hints correctly say "Go LOWER" when my guess is too high, and the New Game button respects the current difficulty. AI helped design the new tests by suggesting which scenarios to cover — specifically the hint direction tests and the difficulty range comparison test — which caught the swapped-message bug even before running the app.

---

## 4. What did you learn about Streamlit and state?

Streamlit works differently from most web frameworks: every time a user interacts with a widget (clicks a button, types in a text box), the entire Python script re-runs from top to bottom. This means any variable you define normally will be reset to its initial value on every interaction — which is exactly why the secret number kept changing every time you clicked "Submit" in the broken version. To persist values across these reruns, Streamlit provides `st.session_state`, a dictionary-like object that survives re-runs for the duration of a browser session. The fix is to write to `st.session_state` on first run and read from it on subsequent runs, using `if "key" not in st.session_state:` guards, which is the pattern already used correctly in `app.py` for `secret`, `attempts`, `score`, `status`, and `history`.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing **targeted tests for each specific bug before fixing it** — a lightweight form of test-driven debugging. Having a test that fails on the broken behavior and passes after the fix gives you a clear, repeatable "before and after" signal that the fix worked, and it also documents the bug for future maintainers.

Next time I work with AI on a debugging task, I would give the AI a narrower scope earlier — rather than asking it to analyze the whole file at once, I'd focus it on one function at a time and explicitly ask it to distinguish between "confirmed bug" and "suspicious but possibly intentional." This would reduce false positives like the scoring asymmetry issue.

This project changed the way I think about AI-generated code: I now treat it as a "first draft that needs review" rather than a working implementation. The bugs in this codebase weren't random — they were exactly the kind of subtle logic errors (swapped conditions, hardcoded values, type inconsistencies) that an LLM might introduce by reasoning at a high level without carefully checking all the edge cases, which means human review is not optional but essential.
