def morse_translator(text):
    morse_code_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
        'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
        'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.'
    }

    translated_text = []
    words = text.split()

    for word in words:
        morse_word = []
        for char in word:
            if char.upper() in morse_code_dict:
                morse_word.append(morse_code_dict[char.upper()])
        translated_text.append(' '.join(morse_word))

    return ' / '.join(translated_text)

# Example usage:
input_text = "Hello World"
result = morse_translator(input_text)
print(result)