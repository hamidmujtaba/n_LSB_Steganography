import cv2
import numpy as np

from consts import MASK_ZERO_VALUES, N_LSB
from utils import binary_value, read_n_bits


# TODO #1: Make this application run through terminal with parameters of cover and secret data

def embed_text():
    with open('sample_secret_msg.txt', 'rb') as secret_file:
        secret = secret_file.read()

    assert len(secret) > 0, "Error: Message length is zero!"
    total_secret_bytes = binary_value(len(secret), 16)

    secret_msg_bitstream = ""
    for char in secret:
        c = ord(char)
        secret_msg_bitstream += binary_value(c, 8)

    secret_bitstream = total_secret_bytes + secret_msg_bitstream
    n_bits_split_secret_bitstream = [secret_bitstream[i:i+N_LSB] for i in range(0, len(secret_bitstream), N_LSB)]

    cover_img = cv2.imread('sample_cover.png', cv2.IMREAD_GRAYSCALE)
    cover_width, cover_height = cover_img.shape
    assert cover_width >= 480, "Error: Cover image width less than minimum (480)"
    assert cover_height >= 480, "Error: Cover image height less than minimum (480)"

    current_index = 0
    embedding_complete = False
    for x, row in enumerate(cover_img):
        for y, pixel in enumerate(row):
            if current_index == len(n_bits_split_secret_bitstream):
                embedding_complete = True
                break

            pixel = np.uint8(pixel & MASK_ZERO_VALUES[N_LSB])
            pixel = np.uint8(pixel | int(n_bits_split_secret_bitstream[current_index], 2))

            cover_img[x][y] = pixel
            current_index += 1

        if embedding_complete:
            break

    cv2.imwrite("stego_img.png", cover_img)


def embed_img():
    secret_img = cv2.imread('sample_secret_img.jpg', cv2.IMREAD_GRAYSCALE)
    width, height = secret_img.shape

    width = binary_value(width, 16)
    height = binary_value(height, 16)

    secret_bitstream = ""
    for row in secret_img:
        for pixel in row:
            pixel = pixel >> (8-N_LSB)
            secret_bitstream += '{:0{N}b}'.format(np.uint8(pixel), N=N_LSB)

    secret_bitstream = width + height + secret_bitstream

    n_bits_split_secret_bitstream = [secret_bitstream[i:i+N_LSB] for i in range(0, len(secret_bitstream), N_LSB)]

    cover_img = cv2.imread('sample_cover.png', cv2.IMREAD_GRAYSCALE)
    cover_width, cover_height = cover_img.shape
    assert cover_width >= 480, "Error: Cover image width less than minimum (480)"
    assert cover_height >= 480, "Error: Cover image height less than minimum (480)"

    current_index = 0
    embedding_complete = False
    for x, row in enumerate(cover_img):
        for y, pixel in enumerate(row):
            if current_index == len(n_bits_split_secret_bitstream):
                embedding_complete = True
                break

            pixel = np.uint8(pixel & MASK_ZERO_VALUES[N_LSB])
            pixel = np.uint8(pixel | int(n_bits_split_secret_bitstream[current_index], 2))

            cover_img[x][y] = pixel
            current_index += 1

        if embedding_complete:
            break

    cv2.imwrite("stego_img.png", cover_img)


def extract_img():
    stego_img = cv2.imread('stego_img.png', cv2.IMREAD_GRAYSCALE)

    # Read first 2 bytes : Size of text in bytes
    img_shape = read_n_bits(stego_img, n=32)
    width = int(img_shape[:16], 2)
    height = int(img_shape[16:], 2)

    # Read secret data
    secret_data = read_n_bits(stego_img, n=(width * height) * N_LSB + 32, offset=32, last_bits=True)

    # Split bitstream receieved in multiples of N_LSB to convert to bytes
    byte_split_secret_bitstream = [secret_data[i:i + N_LSB] for i in range(0, len(secret_data), N_LSB)]

    for index, _byte in enumerate(byte_split_secret_bitstream):
        _byte = (int(_byte, 2) << (8-N_LSB))
        byte_split_secret_bitstream[index] = _byte

    secret_img = np.array([byte_split_secret_bitstream[i:i + height] for i in xrange(0, len(byte_split_secret_bitstream), height)])

    cv2.imwrite("extracted_img.png", secret_img)


def extract_text():
    stego_img = cv2.imread('stego_img.png', cv2.IMREAD_GRAYSCALE)

    # Read first 2 bytes : Size of text in bytes
    no_of_secret_bytes = int(read_n_bits(stego_img, n=2*8), 2)

    # Read secret data
    secret_data = read_n_bits(stego_img, n=(no_of_secret_bytes + 2) * 8, offset=2*8, last_bits=True)

    # Split bitstream receieved in multiples of 8 to convert to bytes
    byte_split_secret_bitstream = [secret_data[i:i + 8] for i in range(0, len(secret_data), 8)]

    secret_text = ""
    for _byte in byte_split_secret_bitstream:
        secret_text += chr(int(_byte, 2))  # Every chars concatenated to str
    print secret_text


def main():
    embed_text()
    extract_text()

    embed_img()
    extract_img()


if __name__=="__main__":
    main()
