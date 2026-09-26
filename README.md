# Secret-Inside-Image-

Python tool for encryption text using **AES-256-GCM** with **PBKDF2** key derivation, to hidden into image pixels using **LSB (Least Significant Bit)** Steganography.

## Features

- **Authenticated Encryption**: Uses `AES-256-GCM` to ensure message confidentiality and integrity.
- **Strong Key Derivation**: Employs `PBKDF2HMAC` with `SHA-256` and $600,000$ iterations to protect against brute-force attacks.
- **LSB Image Steganography**: Hides bits directly into the red, green, and blue (RGB) color channels of PNG images.


## Requirements

Ensure you have Python 3 installed, along with the required libraries:

```bash
pip install pillow cryptography 
```

## How to use
1-Place the PNG image same fille project and name it ```input.png```.

2-Run the script:
```bash
python3 main.py
```
3-**Choose an option**:
Option 1 (Encrypt): Enter your secret message and set a password. The output will be saved as ```output.png ```.

Option 2 (Decrypt): Load ```output.png ```, enter the correct password, and extract your original message.


## Security & Mechanics

1. **Encryption Flow**:
   - `Plaintext` -> `PBKDF2 Key (Salt + Password)` -> `AES-GCM Encryption` -> `Payload (Length + Salt + Nonce + Ciphertext)`

2. **Embedding Flow**:
   - `Payload Bits` -> `Replaces LSBs of R, G, B image pixels`
  





