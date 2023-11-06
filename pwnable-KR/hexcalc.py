import re, sys

def HexCalculator(hex1: str, hex2: str, operator: str) -> int:
    if operator == "+":
        return int(hex1.replace('0x', ''), 16) + int(hex2.replace('0x', ''), 16)
    elif operator == "-":
        return int(hex1.replace('0x', ''), 16) - int(hex2.replace('0x', ''), 16)
    elif operator == "*":
        return int(hex1.replace('0x', ''), 16) * int(hex2.replace('0x', ''), 16)
    elif operator == "/":
        return int(hex1.replace('0x', ''), 16) / int(hex2.replace('0x', ''), 16)
    elif operator == "^":
        return int(hex1.replace('0x', ''), 16) / int(hex2.replace('0x', ''), 16)
    else:
        sys.exit("Error:", hex1, operator, hex2)

def HexXOR(hex1: str, hex2: str):
    i1 = int(hex1.replace("0x", ""), 16)
    i2 = int(hex2.replace("0x", ""), 16)
    return i1 ^ i2

def PrintOutResult(mres):
    print("Integer: {}".format(str(mres)))
    print("Hex: {}".format(hex(mres)))

if len(sys.argv) == 2:
    print("Math:", sys.argv[1])
    if re.match('^0x{0,1}[0-9A-Fa-f]+[\+\*\/\-]0x{0,1}[0-9A-Fa-f]+$', sys.argv[1], re.IGNORECASE):
        result = re.search('^(0x{0,1}[0-9A-Fa-f]+)([\+\*\/\-])(0x{0,1}[0-9A-Fa-f]+)$', sys.argv[1], re.IGNORECASE)
        hex1 = result.group(1)
        operator = result.group(2)
        hex2 = result.group(3)
        mres = HexCalculator(hex1, hex2, operator)
        PrintOutResult(mres)
    else:
        sys.exit("Wrong math.")
elif len(sys.argv) == 4 and sys.argv[2].lower() == "xor":
    print("Math: {} {} {}".format(sys.argv[1], sys.argv[2], sys.argv[3]))
    if re.match('^[0-9A-Fa-f]+$', sys.argv[1], re.IGNORECASE) and re.match('^[0-9A-Fa-f]+$', sys.argv[3], re.IGNORECASE):
        mres = HexXOR(sys.argv[1], sys.argv[3])
        PrintOutResult(mres)
    else:
        sys.exit("Wrong Hex format.")
else:
    sys.exit("Wrong Argument.")