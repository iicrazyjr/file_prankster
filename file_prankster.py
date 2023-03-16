import py7zr, binascii, hashlib
import random, os
import argparse

names = [
    "data1.data",
    "data2.data",
    "data3.data",
    "data4.data",
    "data5.data",
    "data6.data",
    "data7.data",
    "data8.data",
    "data9.data"
]

hashes = list(map(lambda name: hashlib.sha1(name.encode()).hexdigest(), names))
def compress(hidden_file, compress_number, compressed_name="the_final.data"):
    with py7zr.SevenZipFile(compressed_name, 'w') as archive:
        archive.writeall(hidden_file)
        
    for _ in range(0, compress_number-1):
        randomName = random.choice(hashes)
        while compressed_name == randomName:
            randomName = random.choice(hashes)

        with py7zr.SevenZipFile(randomName, 'w') as archive:
            archive.writeall(compressed_name)

        os.remove(compressed_name)
        compressed_name = randomName

    with open(compressed_name, "rb") as f:
        data = f.read()

    hex_data = binascii.hexlify(data)
    os.remove(compressed_name)

    compressed_name = "challenge.data"
    with open(compressed_name, "wb") as f:
        f.write(hex_data)

    print(f"[*] {hidden_file} ultra compressed! on {compressed_name}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="file_prankster.py",
        description="play pranks on your friends by compressing files",
        formatter_class=argparse.HelpFormatter,
        exit_on_error=True,
        add_help=True
    )

    parser.add_argument('-f', '--file', required=True, type=str, help="text file to hide")
    parser.add_argument('-n', '--number', type=int, default=4, help="amount of compressed files (default: %(default)s)")
    args = parser.parse_args()

    filename = args.file
    amount_compress = args.number

    if not os.path.exists(filename):
        raise FileNotFoundError("File not found on current path")
    
    compress(filename, amount_compress)
