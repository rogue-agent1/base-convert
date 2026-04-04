#!/usr/bin/env python3
"""base_convert - Number base converter and bit manipulator.

Convert between bases (2-64), inspect binary, and do bitwise ops. Zero deps.
"""

import argparse
import sys

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"


def to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"
    neg = n < 0
    n = abs(n)
    result = []
    while n:
        result.append(DIGITS[n % base])
        n //= base
    return ("-" if neg else "") + "".join(reversed(result))


def from_base(s: str, base: int) -> int:
    neg = s.startswith("-")
    s = s.lstrip("-")
    n = 0
    for c in s:
        idx = DIGITS.index(c) if c in DIGITS else int(c, 36)
        if idx >= base:
            raise ValueError(f"Digit '{c}' invalid for base {base}")
        n = n * base + idx
    return -n if neg else n


def auto_detect(s: str) -> tuple:
    """Auto-detect base from prefix. Returns (value, base)."""
    s = s.strip()
    if s.startswith("0b") or s.startswith("0B"):
        return from_base(s[2:], 2), 2
    if s.startswith("0o") or s.startswith("0O"):
        return from_base(s[2:], 8), 8
    if s.startswith("0x") or s.startswith("0X"):
        return from_base(s[2:], 16), 16
    return int(s), 10


def cmd_convert(args):
    if args.from_base:
        val = from_base(args.number, args.from_base)
    else:
        val, _ = auto_detect(args.number)
    
    if args.to_base:
        print(to_base(val, args.to_base))
    else:
        print(f"  dec: {val}")
        print(f"  hex: {to_base(val, 16)}")
        print(f"  oct: {to_base(val, 8)}")
        print(f"  bin: {to_base(val, 2)}")


def cmd_inspect(args):
    if args.base:
        val = from_base(args.number, args.base)
    else:
        val, _ = auto_detect(args.number)

    bits = val.bit_length() or 1
    widths = [8, 16, 32, 64]
    width = next((w for w in widths if w >= bits), bits)

    print(f"  Value: {val}")
    print(f"  Bits:  {bits}")
    print(f"  Width: {width}")
    binary = format(val & ((1 << width) - 1), f"0{width}b")
    # Group by 8
    grouped = " ".join(binary[i:i+8] for i in range(0, len(binary), 8))
    print(f"  Bin:   {grouped}")
    print(f"  Hex:   {format(val & ((1 << width) - 1), f'0{width//4}X')}")

    if val < 0 or (val > 0 and binary[0] == "1" and width in (8, 16, 32, 64)):
        signed = val if val < 0 else val - (1 << width)
        print(f"  Signed: {signed}")

    # Set bits
    set_bits = [i for i in range(width) if (val >> i) & 1]
    print(f"  Set bits: {set_bits}")


def cmd_bitwise(args):
    a, _ = auto_detect(args.a)
    b, _ = auto_detect(args.b)
    ops = {
        "and": a & b, "or": a | b, "xor": a ^ b,
        "nand": ~(a & b), "nor": ~(a | b),
    }
    if args.op == "all":
        for name, result in ops.items():
            print(f"  {name:>4}: {result} (0x{result & 0xFFFFFFFF:08X})")
    else:
        result = ops[args.op]
        print(result)


def cmd_shift(args):
    val, _ = auto_detect(args.number)
    n = int(args.n)
    if args.dir == "left":
        print(val << n)
    else:
        print(val >> n)


def main():
    p = argparse.ArgumentParser(description="Number base converter & bit tools")
    sub = p.add_subparsers(dest="cmd")

    cp = sub.add_parser("convert", help="Convert between bases")
    cp.add_argument("number", help="Number (auto-detects 0x/0b/0o prefix)")
    cp.add_argument("-f", "--from-base", type=int, help="Source base (2-64)")
    cp.add_argument("-t", "--to-base", type=int, help="Target base (2-64)")

    ip = sub.add_parser("inspect", help="Inspect binary representation")
    ip.add_argument("number")
    ip.add_argument("-b", "--base", type=int)

    bp = sub.add_parser("bitwise", help="Bitwise operations")
    bp.add_argument("a")
    bp.add_argument("op", choices=["and", "or", "xor", "nand", "nor", "all"])
    bp.add_argument("b")

    sp = sub.add_parser("shift", help="Bit shift")
    sp.add_argument("number")
    sp.add_argument("dir", choices=["left", "right"])
    sp.add_argument("n")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        sys.exit(1)
    {"convert": cmd_convert, "inspect": cmd_inspect,
     "bitwise": cmd_bitwise, "shift": cmd_shift}[args.cmd](args)


if __name__ == "__main__":
    main()
