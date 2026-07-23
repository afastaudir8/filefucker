import argparse
import random
# import hashlib
import os
import sys
import re
import time
import shutil

try:
    from tqdm import tqdm
    barInstalled = True
except ModuleNotFoundError:
    barInstalled = False

def arg_parser():
    parser = argparse.ArgumentParser(
        prog='FileFucker',
        description='Corrupts random bytes in a file.'
    )
    parser.add_argument('file', help="File to corrupt", type=str)
    parser.add_argument("-y", "--yes", action='store_true', help="Skips confirmation prompts")
    parser.add_argument("-c", "--count", type=str, default=10 ,help="The number of bytes the script should corrupt. You can add K, M, or G to indicate kilobytes, etc. 1K = 1000. Default is 10")
    parser.add_argument("-s", "--start", type=str, default=256000 ,help="Where the script should start from in bytes. Default is 256000")
    parser.add_argument("-e", "--end", type=str, help="Where to end the corruption. End of file by default")
    parser.add_argument("-S", "--silent", action="store_true", help="Run somewhat silently (no progress bars)")
    parser.add_argument("-r", "--sort", action="store_true", help="Runs the bytes through a sorting algorithm instead of the usual algorithm")
    parser.add_argument("-o", "--output", type=str)
    return parser.parse_args()


def end_check(file, end):
    if not end or int(end) > os.path.getsize(file):
        end = os.path.getsize(file)
    else:
        end = parse_size(end)
    return end

def sanity_check(start, end):
    if end < start:
        print(f"{colours[1]}error: end is smaller than start{colours[0]}")
        exit(1)
    if start < 0:
        print(f"{colours[1]}error: start is negative{colours[0]}")
        exit(1)

def file_write(file, data):
    try:
        with open(file, "r+b") as f:
            f.seek(start)
            if barInstalled:
                with tqdm(total=len(data), unit="B", unit_scale=True) as bar:
                    for i in range(0, len(data), 1024):
                        chunk = data[i:i + 1024]
                        f.write(chunk)
                        bar.update(len(chunk))
            else:
                f.write(data)
            f.close()
    except IOError:
        print(f"{colours[1]}error: I/O error{colours[0]}")
        exit(1)

def fuck_shit_up(data, count):
    for y in tqdm(range(count)) if barInstalled else range(count):
        i = random.randint(0, len(data)-1)
        data[i] = random.randint(0, 255)
    # hash(data, "Output")
    return data

def hash(data, type):
    sum = hashlib.sha256(data)
    print(f"{type} hash: {sum.hexdigest()}")

def parse_size(size):
    try:
        return int(size)
    except ValueError:
        if re.match("^[0-9]+(\\.[0-9+])?[KMGkmg]$", size):
            unit = str(size[-1]).upper()
            size = float(size[:-1])
            match unit:
                case "K":
                    return int(size * 1000)
                case "M":
                    return int(size * 1000000)
                case "G":
                    return int(size * 1000000000)
        else:
            print(f"{colours[1]}error: not a valid number{colours[0]}")
            exit(1)

def file_open(file, start, end):
    try:
        with open(file, "rb") as f:
            f.seek(start)
            if barInstalled:
                data = bytearray()
                size = end-start
                with tqdm(total=size, unit="B", unit_scale=True) as bar:
                    remaining = size

                    while remaining > 0:
                        chunk = f.read(min(1024, remaining))
                        if not chunk:
                            break
                        data.extend(chunk)
                        remaining -= len(chunk)
                        bar.update(len(chunk))
                    # while chunk := f.read(1024):
                    #     data.extend(chunk)
                    #     bar.update(len(chunk))
            else:
                data = bytearray(f.read(end - start))
            f.close()
            return data
    except FileNotFoundError:
        print(f"{colours[1]}error: file not found{colours[0]}")
        exit(1)
    except IOError:
        print(f"{colours[1]}error: problem with file{colours[0]}")
        exit(1)


if __name__ == "__main__":
    print("FileFucker v2")
    print("Made with ♥ by afastaudir8")

    # in order:
    # reset, red, yellow, green
    colours = ["\033[0m", "\033[0;31m", "\033[0;33m", "\033[0;32m"]

    if sys.version_info.minor < 10 or sys.version_info.major < 3:
        print(f"{colours[1]}This version of FileFucker requires Python 3.10 or newer.{colours[0]}")
        exit(1)

    if not barInstalled:
        print(f"{colours[2]}tqdm is not installed, running anyways{colours[0]}")

    args = arg_parser()

    if (not args.yes) and ((not args.output) or os.path.exists(args.output)):
        try:
            answer = input(f"{colours[1]}YOU HAVE ENTERED A COMMAND THAT *WILL* OVERWRITE THE FILE YOU ENTERED.{colours[0]}\nARE YOU ABSOLUTELY SURE YOU WANT TO PROCEED WITH THIS COMMAND\nI AM IN NO WAY RESPONSIBLE FOR DAMAGE YOU MAY CAUSE WITH THIS SCRIPT.\nTYPE y IF YOU ACCEPT\n").lower()
        except KeyboardInterrupt:
            answer = "n"
            print()
        if answer != "y":
            print("Exiting.")
            exit(1)
    print(f"Starting on file {args.file}")
    
    if args.silent:
        barInstalled = False

    start = parse_size(args.start)
    end = end_check(args.file, args.end)
    # end = parse_size(args.end)
    sanity_check(start, end)
    data = file_open(args.file, start, end)
    
    count = parse_size(args.count)

    if (args.sort):
        print(f"Working between {start} and {end}. Sorting {end-start} bytes.")
    else:
        print(f"Working between {start} and {end}. Corrupting {count} bytes.")

    # hash(data, "Input"
    if args.sort:
        data[:] = sorted(data)
    else:
        fuck_shit_up(data, count)
    print("Writing...")
    if not args.output:
        file_write(args.file, data)
    else:
        shutil.copy(args.file, args.output)
        file_write(args.output, data)
    print(f"{colours[3]}We're done here.{colours[0]}")



