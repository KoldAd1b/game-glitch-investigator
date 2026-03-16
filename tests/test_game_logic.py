from logic_utils import check_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"

def test_hint_direction_too_high():
    # FIX verification: when guess is too high, message should tell player to go LOWER
    result = check_guess(80, 50)
    assert result[0] == "Too High"
    assert "LOWER" in result[1]

def test_hint_direction_too_low():
    # FIX verification: when guess is too low, message should tell player to go HIGHER
    result = check_guess(20, 50)
    assert result[0] == "Too Low"
    assert "HIGHER" in result[1]

def test_hard_difficulty_range():
    # FIX verification: Hard mode should have a wider range than Normal (1-200 vs 1-100)
    low, high = get_range_for_difficulty("Hard")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    assert high > normal_high
