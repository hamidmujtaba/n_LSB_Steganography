import numpy as np
from consts import MASK_ONE_VALUES, N_LSB


class SteganographyException(Exception):
    # TODO: Utilize this exception while exception handling
    def __init__(self, message):
        super(SteganographyException, self).__init__(message)


def binary_value(val, bit_size):  # Return the binary value of an int as a byte
    binval = bin(val)[2:]
    if len(binval) > bit_size:
        raise SteganographyException("binary value larger than the expected size")

    while len(binval) < bit_size:
        binval = '0' + binval

    return binval


def read_n_bits(img, n, offset=0, last_bits=False):
    bitstream = ""
    op_complete = False
    for x, row in enumerate(img):
        for y, pixel in enumerate(row):

            if last_bits:

                if len(bitstream) == n:
                    op_complete = True
                    break

                elif len(bitstream) + N_LSB <= n:
                    pixel = np.uint8(pixel & MASK_ONE_VALUES[N_LSB])
                    bitstream += '{:0{N}b}'.format(pixel, N=N_LSB)

                elif len(bitstream) + N_LSB > n:
                    pixel = np.uint8(pixel & MASK_ONE_VALUES[n - len(bitstream)])
                    bitstream += '{:0{N}b}'.format(pixel, N=n - len(bitstream))

            else:
                pixel = np.uint8(pixel & MASK_ONE_VALUES[N_LSB])
                bitstream += '{:0{N}b}'.format(pixel, N=N_LSB)

                if len(bitstream) >= n:
                    op_complete = True
                    break

        if op_complete:
            break

    return bitstream[offset:n]
