""" A Module for OpenCV testing """

import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

os.makedirs("images/", exist_ok=True)
os.makedirs('images/runtime-images/', exist_ok=True)

# constants
WIDTH = 400  # width of image frames
HEIGHT = 400  # height of image frames
BB_PADY = 10  # padding of lower buttons
FILETYPES = [('All files', '*'), ('Image files', '*.png;*.jpg;*.jpeg')]

# Global Variables
oimg = []  # original image read by openCV
mimg = []  # modified image from opencv


# button Functions
def show_error(title, text):
    messagebox.showerror(title, text)


def resize_to_frame(image):
    # to resize image to frame maintaining the aspect ratio
    width, height = image.width, image.height
    while width > WIDTH or height > HEIGHT:
        if width > WIDTH:
            height = (height * WIDTH)//width
            width = WIDTH

        if height > HEIGHT:
            width = (width * HEIGHT)//height
            height = HEIGHT

    return image.resize((width, height))


def show_original_image():
    # to show full size original image
    if len(oimg):
        cv2.imshow('Original Image', oimg)
    else:
        show_error("Error", "Please Open an image first.")


def open_new_image():
    # to open a new image to perform actions on
    filename = filedialog.askopenfilename(
        initialdir='images/', title="Select Image")
    if filename:
        global oimg
        oimg = cv2.imread(filename, -1)
        showoi = ImageTk.PhotoImage(resize_to_frame(Image.open(filename)))
        oidisplay.configure(image=showoi)
        oidisplay.image = showoi


def show_modified_image():
    # to show full size modified image
    if len(mimg):
        cv2.imshow('Processed Image', mimg)
    else:
        show_error("Error", "No Processed Image exists.")


def update_modified_image():
    show_mi = ImageTk.PhotoImage(resize_to_frame(
        Image.open('images/runtime-images/cv2out.png')))
    midisplay.configure(image=show_mi)
    midisplay.image = show_mi


def save_modified_image():
    global mimg
    if len(mimg):
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialdir='images/',
            initialfile='image.png',
            filetypes=FILETYPES
        )
        if filename:
            cv2.imwrite(filename, mimg)
    else:
        show_error("Error", "No Processed Image exists.")


def show_about():
    messagebox.showinfo("About",
                        """A GUI demonstrating various image enhancement
and restoration techniques.
Made by Chirag Goyal.\nEmail: cgoyal_be17@thapar.edu""")

# image enhancement buttons


def show_bandw():
    # for a black and white image
    global oimg, mimg
    if len(oimg):
        mimg = cv2.cvtColor(oimg, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()
    else:
        show_error("Error", "Please open an image first.")


def median_filter():
    # for median filtered image
    global oimg, mimg
    if len(oimg):
        kernel = simpledialog.askinteger("Input",
                                         "Enter Kernel Value for Median Blur",
                                         minvalue=1, initialvalue=5)
        if kernel and kernel % 2 == 1:
            mimg = cv2.medianBlur(oimg, kernel)
            cv2.imwrite('images/runtime-images/cv2out.png', mimg)
            update_modified_image()
        elif kernel:
            show_error("Error",
                       "Kernel value can only be positive odd interger.\
                \nUsing Default Kernel value: 5")
            kernel = 5
            mimg = cv2.medianBlur(oimg, kernel)
            cv2.imwrite('images/runtime-images/cv2out.png', mimg)
            update_modified_image()
        else:
            return
    else:
        show_error("Error", "Please open an image first.")


# image restoration buttons
def gaussian_noise():
    global oimg, mimg
    if len(oimg):
        row, col, ch = oimg.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = oimg + gauss
        mimg = noisy
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()

    else:
        show_error("Error", "Please open an image first.")


def salt_pepper_noise():
    global oimg, mimg
    if len(oimg):
        row, col, ch = oimg.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(oimg)
        # Salt mode
        num_salt = np.ceil(amount * oimg.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in oimg.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount * oimg.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in oimg.shape]
        out[coords] = 0

        mimg = out
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()

    else:
        show_error("Error", "Please open an image first.")


def poisson_noise():
    global oimg, mimg
    if len(oimg):
        vals = len(np.unique(oimg))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(oimg * vals) / float(vals)
        mimg = noisy
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()

    else:
        show_error("Error", "Please open an image first.")


def speckle_noise():
    global oimg, mimg
    if len(oimg):
        row, col, ch = oimg.shape
        gauss = np.random.randn(row, col, ch)
        gauss = gauss.reshape(row, col, ch)
        noisy = oimg + oimg * gauss
        mimg = noisy
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()

    else:
        show_error("Error", "Please open an image first.")


def laplacian_filter():
    global oimg, mimg
    if len(oimg):
        mimg = cv2.Laplacian(oimg, cv2.CV_64F)
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()

    else:
        show_error("Error", "Please open an image first.")


def sobelx():
    global oimg, mimg
    if len(oimg):
        mimg = cv2.Sobel(oimg, cv2.CV_64F, 1, 0, ksize=5)
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()

    else:
        show_error("Error", "Please open an image first.")


def sobely():
    global oimg, mimg
    if len(oimg):
        mimg = cv2.Sobel(oimg, cv2.CV_64F, 0, 1, ksize=5)
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()

    else:
        show_error("Error", "Please open an image first.")


def canny():
    global oimg, mimg
    if len(oimg):
        mimg = cv2.Canny(oimg, 100, 200)
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()

    else:
        show_error("Error", "Please open an image first.")


def negative():
    global oimg, mimg
    if len(oimg):
        mimg = cv2.bitwise_not(oimg)
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()

    else:
        show_error("Error", "Please open an image first.")


def average_blur():
    global oimg, mimg
    if len(oimg):
        mimg = cv2.blur(oimg, (5, 5))
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()

    else:
        show_error("Error", "Please open an image first.")


def bilateral_filtering():
    global oimg, mimg
    if len(oimg):
        mimg = cv2.bilateralFilter(oimg, 9, 75, 75)
        cv2.imwrite('images/runtime-images/cv2out.png', mimg)
        update_modified_image()

    else:
        show_error("Error", "Please open an image first.")


# main window
window = tk.Tk()
window.resizable(width=False, height=False)

# original image Frame
oiFrame = tk.Frame(window, width=WIDTH, height=HEIGHT, bg='brown')
oiFrame.grid(row=0, column=0, sticky='news')

# start image
oi_blank_source = Image.new('RGB', (WIDTH, HEIGHT), "#603678")
oi_blank = ImageTk.PhotoImage(oi_blank_source)
# original image label
oidisplay = tk.Label(oiFrame, image=oi_blank)
oidisplay.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Original image button Frame
obFrame = tk.Frame(window, width=WIDTH, bg='black')
obFrame.grid(row=1, column=0, sticky='news')

# original image buttons
showOI = tk.Button(obFrame, text='Show Full Size Image', pady=BB_PADY,
                   command=show_original_image,
                   font="none 10 normal")
showOI.pack(fill=tk.X)

openImage = tk.Button(obFrame, text='Open Image', pady=BB_PADY,
                      command=open_new_image,
                      font="none 10 normal")
openImage.pack(fill=tk.X)

# modified Image frame
miFrame = tk.Frame(window, width=WIDTH, height=HEIGHT, bg='#046954')
miFrame.grid(row=0, column=1, sticky='news')

# start modified image
mi_blank_source = Image.new('RGB', (WIDTH, HEIGHT), "gray")
mi_blank = ImageTk.PhotoImage(mi_blank_source)
# modified image label
midisplay = tk.Label(miFrame, image=mi_blank)
midisplay.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# modified image button frame
mbFrame = tk.Frame(window, width=WIDTH, bg='dark green')
mbFrame.grid(row=1, column=1, sticky='news')

# modified image buttons
showMI = tk.Button(mbFrame, text='Show Full Size Image', pady=BB_PADY,
                   command=show_modified_image,
                   font="none 10 normal")
showMI.pack(fill=tk.X)

saveImage = tk.Button(mbFrame, text='Save Image', pady=BB_PADY,
                      command=save_modified_image,
                      font="none 10 normal")
saveImage.pack(fill=tk.X)

# Image enhancement Frame
ihFrame = tk.Frame(window, height=HEIGHT, bg='#910a6b')
ihFrame.grid(row=0, column=2, sticky='news')

# Image Enhancement Labels and Buttons
ihLabel = tk.Label(ihFrame, text="Image\n\nEnhancement",
                   padx=50, pady=10, font="none 14 bold",
                   bg='#383838', fg='white')
ihLabel.pack(fill=tk.X)

tk.Button(ihFrame, text="Black and White", pady=4,
          command=show_bandw,
          font='none 9 normal',
          relief=tk.FLAT).pack(fill=tk.X)

tk.Button(ihFrame, text="Median Filter", pady=4,
          command=median_filter,
          font='none 9 normal',
          relief=tk.FLAT,
          bg='#d6d6d6').pack(fill=tk.X)

tk.Button(ihFrame, text="Laplacian Filter", pady=4,
          command=laplacian_filter,
          font='none 9 normal',
          relief=tk.FLAT).pack(fill=tk.X)

tk.Button(ihFrame, text="Sobel X", pady=4,
          command=sobelx,
          font='none 9 normal',
          relief=tk.FLAT,
          bg='#d6d6d6').pack(fill=tk.X)

tk.Button(ihFrame, text="Sobel Y", pady=4,
          command=sobely,
          font='none 9 normal',
          relief=tk.FLAT).pack(fill=tk.X)

tk.Button(ihFrame, text="Canny Edges", pady=4,
          command=canny,
          font='none 9 normal',
          relief=tk.FLAT,
          bg='#d6d6d6').pack(fill=tk.X)

tk.Button(ihFrame, text="Negative Image", pady=4,
          command=negative,
          font='none 9 normal',
          relief=tk.FLAT).pack(fill=tk.X)

tk.Button(ihFrame, text="Average Blur", pady=4,
          command=average_blur,
          font='none 9 normal',
          relief=tk.FLAT,
          bg='#d6d6d6').pack(fill=tk.X)

tk.Button(ihFrame, text="Bilateral Filtering", pady=4,
          command=bilateral_filtering,
          font='none 9 normal',
          relief=tk.FLAT).pack(fill=tk.X)

# Image Restoration Frame
irFrame = tk.Frame(window, height=HEIGHT, bg='#235a7d')
irFrame.grid(row=0, column=3, sticky='news')

# Image Restoration Labels and Buttons
irLabel = tk.Label(irFrame, text="Image\n\nRestoration",
                   padx=50, pady=10, font="none 14 bold",
                   bg='#fffee6', fg='black')
irLabel.pack(fill=tk.X)

tk.Button(irFrame, text="Gaussian Noise", pady=4,
          command=gaussian_noise,
          font="none 9 normal",
          relief=tk.FLAT,
          bg='#d6d6d6').pack(fill=tk.X)

tk.Button(irFrame, text="Salt and Pepper Noise", pady=4,
          command=salt_pepper_noise,
          font="none 9 normal",
          relief=tk.FLAT).pack(fill=tk.X)

tk.Button(irFrame, text="Poisson Noise", pady=4,
          command=poisson_noise,
          font="none 9 normal",
          relief=tk.FLAT,
          bg='#d6d6d6').pack(fill=tk.X)

tk.Button(irFrame, text="Speckle Noise", pady=4,
          command=speckle_noise,
          font="none 9 normal",
          relief=tk.FLAT).pack(fill=tk.X)

# Exit and credits frame
ecFrame = tk.Frame(window, width=WIDTH, bg='red')
ecFrame.grid(row=1, column=2, columnspan=2, sticky='news')

# exit and credit
aboutButton = tk.Button(ecFrame, text='About', pady=BB_PADY,
                        command=show_about,
                        font="none 10 normal")
aboutButton.pack(fill=tk.X)

exitButton = tk.Button(ecFrame, text='Exit', pady=BB_PADY,
                       command=window.destroy,
                       font="none 10 normal")
exitButton.pack(fill=tk.X)

window.mainloop()
