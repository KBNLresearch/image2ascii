from PIL import Image, ImageEnhance


"""
Docs (https://pillow.readthedocs.io/en/stable/reference/ImageEnhance.html):

An enhancement factor of 0.0 gives a solid gray image,
a factor of 1.0 gives the original image, and greater
values increase the contrast of the image.
"""


imageIn = '/home/johan/kb/ascii-art/test-image2ascii/eddy.jpg'
with Image.open(imageIn) as im:
    im.load()
    for i in [1.0, 1.5, 2.0, 3.0]:
        scale_value=i
        im2 = ImageEnhance.Contrast(im).enhance(scale_value)
        fNameOut = "eddy" + str(int(10*i)) + ".jpg"
        im2.save(fNameOut)

