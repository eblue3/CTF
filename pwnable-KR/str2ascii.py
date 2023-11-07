def convert(text: str):
    return ord(text)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        print(convert(sys.argv[1]))
    elif len(sys.argv) > 2:
        sys.exit("Too many Arguments.")
    else:
        text = input("Strings:")
        print(convert(text))