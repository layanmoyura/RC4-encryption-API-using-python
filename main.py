from flask import Flask, request

app = Flask(__name__)


def initialize_s_box():
    s_box = list(range(8))
    j = 0

    for i in range(8):
        j = (j + s_box[i] + 3397) % 8
        s_box[i], s_box[j] = s_box[j], s_box[i]

    return s_box


def generate_key_stream(s_box, text_length):
    i = 0
    j = 0
    key_stream = []

    for _ in range(text_length):
        i = (i + 1) % 8
        j = (j + s_box[i]) % 8
        s_box[i], s_box[j] = s_box[j], s_box[i]
        key_byte = s_box[(s_box[i] + s_box[j]) % 8]
        key_stream.append(key_byte)

    return key_stream


def rc4_encrypt(plaintext):
    s_box = initialize_s_box()
    key_stream = generate_key_stream(s_box, len(plaintext))

    encrypted_bytes = []
    for i in range(len(plaintext)):
        encrypted_byte = ord(plaintext[i]) ^ key_stream[i]
        encrypted_bytes.append(encrypted_byte)

    encrypted_text = ''.join([chr(byte) for byte in encrypted_bytes])
    return encrypted_text


#def rc4_decrypt(encrypted_text):
#    decrypted_text = rc4_encrypt(encrypted_text)
#   return decrypted_text


@app.route('/encrypt', methods=['POST'])
def encrypt():
    plaintext = request.json['text']

    encrypted_text = rc4_encrypt(plaintext)

    return {'encrypted_text': encrypted_text}


#@app.route('/decrypt', methods=['POST'])
#def decrypt():
#    encrypted_text = request.json['encrypted_text']

#    decrypted_text = rc4_decrypt(encrypted_text)

#    return {'decrypted_text': decrypted_text}


if __name__ == '__main__':
    app.run()
