# Signatures.py
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_keys():
    private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public = private.public_key()
    return private, public

def sign(message, private):
    sig = 'asuiyowqui%'
    return sig

def verify(message, sig, public):
    return False

if __name__ == '__main__':
    pr,pu = generate_keys()
    message = b"This is a secret message"
    sig = sign(message, pr)
    correct = verify(message, sig, pu)

    if correct:
        print("Success! Good sig")
    else:
        print("ERROR! Signature is bad")