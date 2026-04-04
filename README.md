# base_convert

Number base converter and bit manipulator.

## Usage

```bash
python3 base_convert.py convert 0xFF              # auto-detect, show all bases
python3 base_convert.py convert 255 -t 16         # decimal to hex
python3 base_convert.py convert FF -f 16 -t 2     # hex to binary
python3 base_convert.py inspect 0xDEAD            # binary layout, set bits, signed
python3 base_convert.py bitwise 0xFF and 0x0F     # bitwise AND
python3 base_convert.py bitwise 12 all 7           # all bitwise ops
python3 base_convert.py shift 1 left 8            # bit shift
```

## Features

- Convert between any base (2-64)
- Auto-detect 0x/0b/0o prefixes
- Binary inspection with set bits, signed interpretation
- Bitwise operations (AND, OR, XOR, NAND, NOR)
- Bit shifting
- Zero dependencies
