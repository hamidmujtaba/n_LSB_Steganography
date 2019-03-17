# This variable specifies no. of LSBs to use
N_LSB = 1

# This variable specifies the secret 'txt' file path
SECRET_TEXT_FILE_PATH = 'sample_secret_msg.txt'

# This variable specifies the secret image file path
SECRET_IMAGE_PATH = 'sample_secret_img.jpg'

#  This variable specifies the cover image file path
COVER_FILE_PATH = 'sample_cover.png'

#  This variable specifies the stego image file path
STEGO_IMAGE_PATH = 'stego_img.png'

# This variable specifies the file path for extracted image from stego object
EXTRACTED_IMG_FILE_PATH = "extracted_img.png"

# Set this flag to 1 to perform operation, 0 to skip
HIDE_TEXT_FILE = 0

# Set this flag to 1 to perform operation, 0 to skip
UNHIDE_TEXT_FILE = 0

# Set this flag to 1 to perform operation, 0 to skip
HIDE_IMAGE_FILE = 0

# Set this flag to 1 to perform operation, 0 to skip
UNHIDE_IMAGE_FILE = 1

# Application specific constants
MASK_ZERO_VALUES = [255, 254, 252, 248, 240, 224, 192, 128, 0]

MASK_ONE_VALUES = [0, 1, 3, 7, 15, 31, 63, 127, 255]
