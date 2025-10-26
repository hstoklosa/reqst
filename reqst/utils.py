import sys


def bout(x): sys.stdout.buffer.write(x)
def out(x): return sys.stdout.write(str(x)+"\n")
def err(x): return sys.stderr.write(str(x)+"\n")
def by_key_lower(item: tuple): key, val = item; return key.lower()