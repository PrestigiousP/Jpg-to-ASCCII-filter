from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageOps
import numpy as np
import cv2
from matplotlib import pyplot as plt

CONST_DICE_VALS = [1, 2, 3, 4, 5, 6]
CONST_ASCII_TEST = ['.', ':', '|', 'U', '$', '@']


def define_steps(val):
    return 256 // val


def calc_range(pix_val, step):
    incr = step
    count = 0
    while pix_val > incr:
        count += 1
        incr += step
        if incr > 255:
            count = 5
            break
    return count


def write_result(res, step):
    f = open("resultFile.txt", "w+")
    for row in res:
        for col in row:
            val = calc_range(col, step)
            # dice_val = CONST_DICE_VALS[val]
            dice_val = CONST_ASCII_TEST[val]
            f.write(str(dice_val) + ' ')
        f.write("\n")
    f.close()


def convert_to_grayscale(img_path):
    im = Image.open(img_path)
    return ImageOps.grayscale(im)


def main():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("jpg",
                                                      "*.jpg"),
                                                     ("png",
                                                      "*.png"),
                                                     ("jpeg",
                                                      "*.jpeg")
                                                     ))
    image = convert_to_grayscale(filename)
    image.save("gray_img.jpg")
    img = cv2.imread("gray_img.jpg")
    res = cv2.resize(img, dsize=(75, 100), interpolation=cv2.INTER_CUBIC)
    single_byte_res = [[col[0] for col in row] for row in res]
    step = define_steps(6)
    # image.show()
    write_result(single_byte_res, step)
    plt.imshow(single_byte_res, interpolation='nearest')
    plt.gray()
    plt.show()


# Create the root window
window = Tk()

# Set window size
window.geometry("600x400")
# Set background color
window.configure(bg='white')

button_explore = Button(window,
                        text="Browse Files",
                        background='White',
                        command=main)

# Display UI elements on the dialog
button_explore.pack()

# Let the window wait for any events
window.mainloop()
