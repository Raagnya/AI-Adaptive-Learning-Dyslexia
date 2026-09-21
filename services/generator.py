import os
from functools import lru_cache

MODEL_NAME = os.getenv("GPT2_MODEL", "gpt2")

@lru_cache(maxsize=1)
def get_pipeline():
    from transformers import pipeline
    return pipeline(
        "text-generation",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME
    )

def build_prompt(difficulty, topic):
    instructions = {
        "easy": "Write one short, simple sentence",
        "medium": "Write one moderately detailed sentence",
        "hard": "Write one longer sentence with more advanced vocabulary"
    }
    instruction = instructions.get(difficulty, instructions["easy"])
    return f"{instruction} about {topic}:"

def clean_generated_text(text, prompt):
    text = text.replace(prompt, "", 1).strip()
    # Keep only the first generated sentence.
    for marker in [".", "!", "?"]:
        idx = text.find(marker)
        if idx != -1:
            return text[:idx + 1].strip()
    return text.strip()

def generate_sentence(difficulty="easy", topic="everyday life"):
    prompt = build_prompt(difficulty, topic)
    try:
        generator = get_pipeline()
        result = generator(
            prompt,
            max_new_tokens=24,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=generator.tokenizer.eos_token_id
        )
        generated = result[0]["generated_text"]
        sentence = clean_generated_text(generated, prompt)
        if sentence:
            return sentence
    except Exception:
        pass

    # Fallback keeps the demo usable if the model is unavailable.
    fallback = {
        "easy": {
            "animals": "The cat is sleeping.",
            "everyday life": "The boy reads a book.",
            "school": "The student opens a book."
        },
        "medium": {
            "animals": "The little dog runs quickly across the garden.",
            "everyday life": "The girl walks carefully to the nearby shop.",
            "school": "The student finishes the science assignment before lunch."
        },
        "hard": {
            "animals": "The curious puppy carefully followed the butterfly across the garden.",
            "everyday life": "The young student organized her books before starting the difficult assignment.",
            "school": "The student completed the challenging experiment and recorded the observations carefully."
        }
    }
    return fallback.get(difficulty, fallback["easy"]).get(
        topic, fallback.get(difficulty, fallback["easy"])["everyday life"]
    )
