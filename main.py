from PIL import Image
import os
from glob import glob

import warnings

# "w"=width, "h"=height, "b"=both, "n"=none
CUSTOM_SCALE = "b"
# width/height character
CUSTOM_WIDTH = 20
CUSTOM_HEIGHT = 10

# Darkest character to the brightest character
CUSTOM_CHARACTERS = "█▓▒░ "


def calc_size(w: int, h: int):
    match CUSTOM_SCALE:
        case "w":
            return (CUSTOM_WIDTH, ((CUSTOM_WIDTH * h) // w))
        case "h":
            return (((CUSTOM_HEIGHT * w) // h), CUSTOM_HEIGHT)
        case "b":
            return (CUSTOM_WIDTH, CUSTOM_HEIGHT)
        case _:
            return (w, h)


def choose_character_for_pixel(pixel_brightness):
    steps = 255 // len(CUSTOM_CHARACTERS)

    # handle max pixel_brightness
    if pixel_brightness == 255:
        return CUSTOM_CHARACTERS[-1]

    return CUSTOM_CHARACTERS[pixel_brightness // steps]


def img_to_ascii(img_path):
    # convert image to grayscale
    gray_img = Image.open(img_path).convert("L")

    # resize image
    width, height = gray_img.size

    # scale image to half height
    half_height = height // 2
    resized_img = gray_img.resize((width, half_height))

    new_size = calc_size(w=resized_img.width, h=resized_img.height)

    resized_image = resized_img.resize(new_size)

    pixels = []
    for y in range(resized_image.height):
        row = ""
        for x in range(resized_image.width):
            # Get the pixel value (0-255) (dark-light)
            pixel = choose_character_for_pixel(resized_image.getpixel((x, y)))
            row += pixel
        pixels.append(row)
    print(f">> Image '{img_path}' converted to ascii")
    return pixels


def ascii_to_file(ascii, file_path):
    with open(file_path, "w") as file:
        for row in ascii:
            file.writelines(row + "\n")
        print(f">> File '{file_path}' filled with ascii")


def main():
    warnings.filterwarnings("ignore")
    imgs_paths = glob("./images/*.png")

    print()

    for img_path in imgs_paths:
        ascii = img_to_ascii(img_path=img_path)

        file_name = os.path.basename(img_path)
        file_path = f"./asciies/{file_name}.txt"
        ascii_to_file(ascii=ascii, file_path=file_path)

    print()
    print("█▓▒░ "[::-1], end="")
    print("█" * 60, end="")
    print("█▓▒░ ")
    print(f"\t{len(imgs_paths)} files converted to ascii art, check 'asciies' folder")
    print("\t\t\tFinished, Enter to Exit")
    print("█▓▒░ "[::-1], end="")
    print("█" * 60, end="")
    input("█▓▒░ ")


if __name__ == "__main__":
    main()
