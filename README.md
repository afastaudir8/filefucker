# FileFucker

## The finest fucker of files

This is a Python utility (if you can even call it that) for 3.10 or newer that corrupts files by replacing random bytes.

I built this specifically for corrupting PSX BIOS files and games, but it will work for any file.

# I AM NOT RESPONSIBLE FOR ANY DAMAGE YOU CAUSE USING THIS SCRIPT, YOU HAVE BEEN WARNED.

## Help dialog

```usage: FileFucker [-h] [-y] [-c COUNT] [-s START] [-e END] [-S] [-o OUTPUT] file

Corrupts random bits in a file. Meant for corrupting PSX BIOS files.

positional arguments:
  file                 File to corrupt

options:
  -h, --help           show this help message and exit
  -y, --yes            Skips confirmation prompts
  -c, --count COUNT    The number of bytes the script should corrupt. You can add K, M, or G to indicate
                       kilobytes, etc. 1K = 1000. Default is 10
  -s, --start START    Where the script should start from in bytes. Default is 256000
  -e, --end END        Where to end the corruption. End of file by default
  -S, --silent         Run somewhat silently (no progress bars)
  -o, --output OUTPUT
```

## Known Issues

Can hog fuck tons of memory if you load large files because everything gets loaded straight to RAM. This will be fixed in v2.

 
