import sys
from pycose.messages import Sign1Message
from pycose.keys.ec2 import EC2Key
from pycose.headers import KID
from pycose.algorithms.cose_algorithms import Es256  # ✅ this is the real implementation

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def load_private_key(pkcs8_path):
    with open(pkcs8_path, "rb") as f:
        return serialization.load_der_private_key(f.read(), password=None, backend=default_backend())

def main():
    if len(sys.argv) != 4:
        print("Usage: python cose_signer.py <input_file> <output_file> <private_key.pk8>")
        sys.exit(1)

    input_file, output_file, private_key_file = sys.argv[1:4]

    with open(input_file, "rb") as f:
        payload = f.read()

    private_key = load_private_key(private_key_file)

    numbers = private_key.private_numbers()
    public_numbers = numbers.public_numbers
    x = public_numbers.x.to_bytes(32, 'big')
    y = public_numbers.y.to_bytes(32, 'big')
    d = numbers.private_value.to_bytes(32, 'big')

    cose_key = EC2Key(crv="P-256", x=x, y=y, d=d)

    msg = Sign1Message(phdr={KID: b"01"}, payload=payload)
    msg.key = cose_key
    msg.alg = Es256  # ✅ ensures .sign() is available

    with open(output_file, "wb") as f:
        f.write(msg.encode())

    print(f"✅ Signed {input_file} → {output_file}")

if __name__ == "__main__":
    main()
