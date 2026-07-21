import argparse
import random
import hashlib
import os
import re
try:
    from tqdm import tqdm
    barInstalled = True
except ModuleNotFoundError:
    barInstalled = False

def arg_parser():
    parser = argparse.ArgumentParser(
        prog='FileFucker',
        description='Corrupts random bits in a file. Meant for corrupting PSX BIOS files.'
    )
    parser.add_argument('file', help="File to corrupt", type=str)
    parser.add_argument("-y", "--yes", action='store_true', help="Skips confirmation prompts")
    parser.add_argument("-c", "--count", type=str, default=10 ,help="The number of bytes the script should corrupt. You can add K, M, or G to indicate kilobytes, etc. 1K = 1000. Default is 10")
    parser.add_argument("-s", "--start", type=str, default=256000 ,help="Where the script should start from in bytes. Default is 256000")
    parser.add_argument("-e", "--end", type=str, help="Where to end the corruption. End of file by default")
    parser.add_argument("-S", "--silent", action="store_true", help="Run somewhat silently (no progress bars)")
    parser.add_argument("-o", "--output", type=str)
    return parser.parse_args()




# def file_check(file):
#     try:
#         with open(file, "rb") as f:
#             f.read()
#     except FileNotFoundError:
#         print("error: file not found")
#         exit(1)
def end_check(data, end):
    if not end or end > len(data):
        end = len(data)
    else:
        end = parse_size(end)
    return end

def sanity_check(start, end):
    if end < start:
        print("error: end is smaller than start")
        exit(1)
    if start < 0:
        print("error: start is negative")
        exit(1)

def file_write(file, data):
    try:
        with open(file, "wb") as f:
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
        print("error: I/O error")
        exit(1)

def fuck_shit_up(data, count, start, end):
    for y in tqdm(range(count)) if barInstalled else range(count):
        i = random.randint(start, end)
        data[i] = random.randint(0, 255)
    hash(data, "Output")
    return data

def hash(data, type):
    sum = hashlib.sha256(data)
    print(f"{type} hash: {sum.hexdigest()}")

def parse_size(size):
    try:
        return int(size)
    except ValueError:
        if re.match("^[0-9]+(\\.[0-9+])?[KMGkmg]$", size):
            unit = size[-1]
            size = float(size[:-1])
            match unit:
                case "K" | "k":
                    return int(size * 1000)
                case "M" | "m":
                    return int(size * 1000000)
                case "G" | "g":
                    return int(size * 1000000000)
        else:
            print("error: not a valid number")

def file_open(file):
    try:
        with open(file, "rb") as f:
            if barInstalled:
                data = bytearray()
                size = os.path.getsize(file)
                with tqdm(total=size, unit="B", unit_scale=True) as bar:
                    while chunk := f.read(1024):
                        data.extend(chunk)
                        bar.update(len(chunk))
            else:
                data = bytearray(f.read())
            f.close()
            return data
    except FileNotFoundError:
        print("error: file not found")
        exit(1)
    except IOError:
        print("error: problem with file")
        exit(1)


if __name__ == "__main__":
    print("FileFucker v1")
    if not barInstalled:
        print("tqdm is not installed, running anyways")
    args = arg_parser()
    if (not args.yes) and ((not args.output) or os.path.exists(args.output)):
        answer = input(f"YOU HAVE ENTERED A COMMAND THAT *WILL* OVERWRITE THE FILE YOU ENTERED.\nARE YOU ABSOLUTELY SURE YOU WANT TO PROCEED WITH THIS COMMAND\nI AM IN NO WAY RESPONSIBLE FOR DAMAGE YOU MAY CAUSE WITH THIS SCRIPT.\nTYPE y IF YOU ACCEPT\n").lower()
        if answer != "y":
            print("Exiting.")
            exit(1)
    print(f"Starting on file {args.file}")
    
    if args.silent:
        barInstalled = False

    data = file_open(args.file)
    start = parse_size(args.start)
    end = end_check(data, args.end)
    sanity_check(start, end)
    count = parse_size(args.count)
    
    print(f"Working between {start} and {end}. Corrupting {count} bytes.")

    hash(data, "Input")
    fuck_shit_up(data, count, start, end)
    if not args.output:
        file_write(args.file, data)
    else:
        file_write(args.output, data)
    print("We're done here.")



