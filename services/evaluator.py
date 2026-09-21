import re
from difflib import SequenceMatcher

def normalize(text):
    return re.sub(r"\s+", " ", re.sub(r"[^a-zA-Z0-9\s']", "", text.lower())).strip()

def evaluate_response(expected, actual):
    expected_n = normalize(expected)
    actual_n = normalize(actual)

    if not expected_n:
        return {"score": 0, "feedback": "No expected sentence was provided."}

    score = round(SequenceMatcher(None, expected_n, actual_n).ratio() * 100)

    if score >= 90:
        feedback = "Excellent! Your response is very close to the expected sentence."
    elif score >= 70:
        feedback = "Good attempt. Review the words that differ from the expected sentence."
    elif score >= 50:
        feedback = "Keep practicing. Some words or spellings differ from the expected sentence."
    else:
        feedback = "Let's practice this sentence again. Check the spelling and word order."

    return {"score": score, "feedback": feedback}
