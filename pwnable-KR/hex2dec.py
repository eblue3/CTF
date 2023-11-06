def convert(hex: str):
    return int(hex, 16)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        print(convert(sys.argv[1]))
    elif len(sys.argv) > 2:
        sys.exit("Too many Arguments.")
    else:
        hex = input("Hex strings:")
        print(convert(hex))