from trans import Translator
import sys

allowed_languages = [
    'Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
    'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish'
]

translator = Translator(allowed_languages)

args = sys.argv
if args[1].title() not in allowed_languages:
    print(f"Sorry, the program doesn't support {args[1]}")
    exit()

if args[2].title() not in allowed_languages and args[2] != 'all':
    print(f"Sorry, the program doesn't support {args[2]}")
    exit()

translator.user_language = allowed_languages.index(args[1].title())
if args[2] == 'all':
    translator.target_language = 0
else:
    translator.target_language = allowed_languages.index(args[2].title()) + 1

if len(args) > 3:
    translator.translate_word = args[3]
else:
    print("Sorry, you haven't entered a word")
    exit()

translator.get_translate()
