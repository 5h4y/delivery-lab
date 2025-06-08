def text_to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_string):
    try:
        chars = binary_string.split()
        return ''.join(chr(int(b, 2)) for b in chars)
    except ValueError:
        return "Invalid binary input. Needs to be space-separated 8-bit binary numbers, get it together."

def main():
    print("=== Text ↔ Binary Converter ===")
    print("1. Text to Binary")
    print("2. Binary to Text")
    choice = input("Select mode (1 or 2): ").strip()

    if choice == '1':
        text = input("Enter text to convert: ").strip()
        print(f"Binary Output:\n{text_to_binary(text)}")
    elif choice == '2':
        binary_input = input("Enter binary: ").strip()
        print(f"Text Output:\n{binary_to_text(binary_input)}")
    else:
        print("Not a valid choice.")

if __name__ == "__main__":
    main()
