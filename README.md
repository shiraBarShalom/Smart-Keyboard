<!-- Center the image and make it circular -->
<p align="center">
  <img src="keyboard_demo.png" alt="Smart Keyboard" width="150" style="border-radius:50%;">
</p>

<h1 align="center">Smart Keyboard Project</h1>

<p align="center">
A smart Hebrew-English keyboard that automatically detects the input language and corrects typing errors.
</p>

## Description
This project is a custom smart keyboard that automatically detects whether the user is typing in Hebrew or English and switches the layout seamlessly. It also provides **context-aware corrections**, ensuring that mistyped words in the wrong keyboard layout are corrected automatically.

The main goal of this project is to **improve typing efficiency and accuracy** for bilingual users who switch frequently between Hebrew and English.

## Problem Statement
Typing in multiple languages can be error-prone, especially when the wrong keyboard layout is active. Common issues include:
- Hebrew words typed in an English layout
- Repeated letters due to fast typing
- Contextual errors in bilingual sentences (e.g., Hebrew-English-Hebrew sequences)

These issues reduce typing speed and introduce errors in daily computer use.

## Solution
The keyboard software solves these problems by:
1. Monitoring user input in real-time using Python and the `pynput` library.
2. Detecting word boundaries and checking each word against **Hebrew and English dictionaries**.
3. Automatically translating English-typed words into Hebrew layout when appropriate.
4. Normalizing repeated letters in mistyped words.
5. Applying **context-aware corrections** for patterns like Hebrew-English-Hebrew.
6. Replacing the text dynamically using simulated keypresses to correct the word.

## Features
- Automatic language detection (Hebrew/English)
- Context-aware word correction
- Efficient key mapping logic to improve typing accuracy
- Maintains a short history of last words for contextual fixes

## Technologies Used
- Python 3
- `pynput` for keyboard input monitoring and text replacement
- `re` for regular expressions and text normalization
- Custom Hebrew and English dictionaries for word validation

## Usage
1. Ensure Python 3 is installed on your system.
2. Place the Hebrew and English dictionary files (`he_smart.txt` and `google-10000-english.txt`) in the project directory.
3. Run the main script:

```bash
python keyboard_project.py
