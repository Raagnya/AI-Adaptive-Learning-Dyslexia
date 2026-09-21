LEVELS = ["easy", "medium", "hard"]

def update_difficulty(current, score):
    current = current if current in LEVELS else "easy"
    index = LEVELS.index(current)

    if score >= 85 and index < len(LEVELS) - 1:
        index += 1
    elif score < 60 and index > 0:
        index -= 1

    return LEVELS[index]
