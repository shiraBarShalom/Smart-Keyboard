import re
import time
from pynput import keyboard


# ==============================
# Configuration & Global State
# ==============================

current_word = []
controller = keyboard.Controller()
keys_to_ignore = 0

# Stores last 3 words:
# Each item: {"raw": str, "clean": str, "hebrew": bool}
history = []


# ==============================
# Dictionary Loading
# ==============================

def load_words(filename):
    """
    Load words from a text file.
    Removes Hebrew niqqud and returns a set of lowercase words.
    """
    words = set()
    niqqud_pattern = re.compile(r'[\u0591-\u05C7]')

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip().lower()
                word = niqqud_pattern.sub('', word)

                if word:
                    words.add(word)

    except FileNotFoundError:
        print(f"Error: {filename} not found.")

    return words


# ==============================
# Keyboard Mapping
# ==============================

ENG_TO_HEB = {
    'q': '/', 'w': "'", 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט',
    'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
    'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע',
    'h': 'י', 'j': 'ח', 'k': 'ל', 'l': 'ך', ';': 'ף',
    'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה',
    'b': 'נ', 'n': 'מ', 'm': 'צ',
    ',': 'ת', '.': 'ץ', '/': '.'
}


print("Loading dictionaries...")
HEBREW_WORDS = load_words("he_smart.txt")
ENGLISH_WORDS = load_words("google-10000-english.txt")
print("System Ready! Context-aware English→Hebrew Fix.")


# ==============================
# Translation & Normalization
# ==============================

def translate_to_hebrew(word):
    """
    Translate an English-typed word into Hebrew layout
    using keyboard mapping.
    """
    return "".join(ENG_TO_HEB.get(c, c) for c in word)


def normalize_repeated_letters(word):
    """
    Remove trailing repeated letters if the word
    is not found in the Hebrew dictionary.
    """
    while len(word) > 2 and word[-1] == word[-2] and word not in HEBREW_WORDS:
        word = word[:-1]

    return word


# ==============================
# Text Replacement Logic
# ==============================

def replace_text(old_text, new_text):
    """
    Replace typed text by simulating backspaces
    and typing new text.
    """
    global keys_to_ignore

    back_count = len(old_text)
    type_count = len(new_text)

    keys_to_ignore = back_count + type_count

    # Delete old text
    for _ in range(back_count):
        controller.press(keyboard.Key.backspace)
        controller.release(keyboard.Key.backspace)
        time.sleep(0.002)

    # Type corrected text
    controller.type(new_text)


# ==============================
# Word Checking Logic
# ==============================

def check_word():
    """
    Check the current typed word.
    If it looks like mistyped Hebrew (typed in English layout),
    attempt automatic correction.
    """
    global current_word, history

    raw_word = "".join(current_word).lower()

    if not raw_word:
        return

    clean_word = raw_word.strip("!@#$%^&*()_+-=[]{}|:?<>")
    is_hebrew = False

    # Case 1: Word already valid Hebrew
    if clean_word in HEBREW_WORDS:
        is_hebrew = True

    # Case 2: Word not valid English → try Hebrew translation
    elif clean_word not in ENGLISH_WORDS:
        translated = translate_to_hebrew(clean_word)

        if translated not in HEBREW_WORDS:
            translated = normalize_repeated_letters(translated)

        if translated in HEBREW_WORDS:
            print(f"Fixing: {raw_word} -> {translated}")

            replace_text(raw_word + " ", translated + " ")

            raw_word = translated
            clean_word = translated
            is_hebrew = True

    # Save word to history
    history.append({
        "raw": raw_word,
        "clean": clean_word,
        "hebrew": is_hebrew
    })

    # Keep only last 3 words
    if len(history) > 3:
        history.pop(0)


def check_context():
    """
    If pattern is:
    Hebrew - English - Hebrew
    then try translating the middle word.
    """
    global history

    if len(history) < 3:
        return

    w1, w2, w3 = history

    if w1["hebrew"] and w3["hebrew"] and not w2["hebrew"]:

        translated = translate_to_hebrew(w2["clean"])

        if translated in HEBREW_WORDS:
            old_text = f"{w1['raw']} {w2['raw']} {w3['raw']} "
            new_text = f"{w1['raw']} {translated} {w3['raw']} "

            print(f"Context Fix: {w2['raw']} -> {translated}")

            replace_text(old_text, new_text)

            # Update history
            w2["raw"] = translated
            w2["clean"] = translated
            w2["hebrew"] = True


# ==============================
# Keyboard Event Handling
# ==============================

def on_press(key):
    """
    Handle key press events.
    Detect word boundaries and trigger checks.
    """
    global current_word, keys_to_ignore

    if keys_to_ignore > 0:
        keys_to_ignore -= 1
        return

    try:
        # Space indicates end of word
        if key == keyboard.Key.space:
            check_word()
            check_context()
            current_word = []
            return

        # Handle backspace
        if key == keyboard.Key.backspace:
            if current_word:
                current_word.pop()
            return

        # Regular character input
        if hasattr(key, 'char') and key.char:
            current_word.append(key.char.lower())

    except Exception:
        pass


# ==============================
# Main Execution
# ==============================

if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
