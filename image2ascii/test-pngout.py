import os
from html2image import Html2Image
from PIL import Image, ImageEnhance, ImageOps

widthRatio = 2.2

imageIn = '/home/johan/kb/ascii-art/test-image2ascii/eddy.jpg'
nameOutHtml = 'ascii.html'
nameOutPng = 'ascii.png'
pathOut = '/home/johan/kb/ascii-art/test-2/'
htmlOut = '/home/johan/kb/ascii-art/test-2/ascii.html'
pngOut = os.path.join(pathOut, nameOutPng)

with Image.open(imageIn) as im:
    im.load()
    width, height = im.size
    print('width: ' + str(width) + ' height: ' + str(height))

# Convert HTML to PNG
hti = Html2Image(size=(width + 100, height + 100), output_path=pathOut)
hti.screenshot(html_file=htmlOut,
                save_as=nameOutPng)

