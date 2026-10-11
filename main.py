import os
import pyfiglet
from PIL import Image
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

INPUT_IMAGE = "input.png"
OUTPUT_IMAGE = "output.png"

def get_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000
    )

    return kdf.derive(password.encode())

def bytes_to_bits(data):
    bits = []

    for byte in data:

        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    return bits

def bits_to_bytes(bits):

    data = bytearray()

    for i in range(0, len(bits), 8):

        byte = 0

        for bit in bits[i:i + 8]:
            byte = (byte << 1) | bit

        data.append(byte)

    return bytes(data)

def encrypt():

    text = input("\033[1;32mEnter Your Message: \033[0m")
    password = input("\033[1;31mEnter Password: \033[0m")

    salt = os.urandom(16)
    key = get_key(password, salt)
    aes = AESGCM(key)
    nonce = os.urandom(12)

    encrypted = aes.encrypt(
        nonce,
        text.encode("utf-8"),
        None
    )

    data = salt + nonce + encrypted

    data_length = len(data)

    length = data_length.to_bytes(4, byteorder="big")

    complete_data = length + data

    bits = bytes_to_bits(complete_data)

    image = Image.open(INPUT_IMAGE).convert("RGB")
    pixels = image.load()

    capacity = image.width * image.height * 3

    if len(bits) > capacity:

        print("image is small ")
        return

    index = 0

    for y in range(image.height):

        for x in range(image.width):

            r, g, b = pixels[x, y]

            if index < len(bits):

                r = (r & 254) | bits[index]
                index += 1
            if index < len(bits):
                g = (g & 254) | bits[index]
                index += 1
            if index < len(bits):
                b = (b & 254) | bits[index]
                index += 1

            pixels[x, y] = (r,g,b)            

            if index >= len(bits):
                break

        if index >= len(bits):
            break

    image.save(OUTPUT_IMAGE)
    print("\033[1;32mEncryption completed successfully\033[0m")
    print("image:", OUTPUT_IMAGE)

def decrypt():

    password = input("Enter Password:")

    image = Image.open(OUTPUT_IMAGE).convert("RGB")

    pixels = image.load()

    length_bits = []

    for y in range(image.height):
        for x in range(image.width):

            r, g, b = pixels[x,y]

            length_bits.append(r & 1)

            if len(length_bits) >= 32:
                break

            length_bits.append(g & 1)

            if len(length_bits) >= 32:
                break

            length_bits.append(b & 1)

            if len(length_bits) >= 32:
                break

        if len(length_bits) >= 32:
            break

    length_bytes = bits_to_bytes(length_bits)

    data_length = int.from_bytes(
        length_bytes,
        byteorder="big"
    )    

    print("data size:", data_length, "bytes")

    total_bits = (4 + data_length) * 8

    bits = []

    for y in range(image.height):

        for x in range(image.width):

            r, g, b = pixels[x,y]

            bits.append(r & 1)

            if len(bits) >= total_bits:
                break

            bits.append(g & 1)

            if len(bits) >= total_bits:
                break

            bits.append(b & 1)

            if len(bits) >= total_bits:
                break

        if len(bits) >= total_bits:
            break


    complete_data = bits_to_bytes(bits)

    data = complete_data[4:4 + data_length]

    salt = data[:16]
    nonce = data[16:28]
    encrypted = data[28:]

    key = get_key(password, salt)

    aes = AESGCM(key)

    try:

        text = aes.decrypt(
            nonce,
            encrypted,
            None
        )

        print("\033[1;32mDecryption completed successfully\033[0m")
        print('------------------------')
        print(text.decode('utf-8'))
        print('------------------------')
        

    except Exception:

        print("\033[1;31mIncorrect password\033[0m")    


print("\033[1;32m")
print(pyfiglet.figlet_format("A Secret Inside Image"))
print("\033[0m")

print("\033[1;31m")
print("1-Encrypt message into image")
print("2-Decrypt message from image")
print("\033[0m")

choice = input("\n Select option: ")

if choice == "1":
    encrypt()
elif choice == "2":
    decrypt()
else:
    print("invalid selection")        
            