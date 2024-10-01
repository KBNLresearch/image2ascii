#! /usr/bin/env python3

import os
import shutil
import uuid
import base64
import time
import justpy as jp
from ascii_magic import AsciiArt
from html2image import Html2Image
from PIL import Image

__version__ = '0.1.0'

# Set following variables as global as sharing them otherwise within
# Justpy is a major PITA!
columnsOut = 150
widthRatio = 2.2
colourFlag = True

def asciifyToFile(self, msg):
    """Create ASCII art from file, write result to HTML file and generate link
    to result (which opens in a new browser tab)"""
    global columnsOut
    global widthRatio
    self.out_div.delete_components()
    imageIn = os.path.abspath(self.imageRef[0].text)
    nameOut = 'ascii.html'
    htmlOut = os.path.abspath(nameOut)
    with Image.open(imageIn) as im:
        im.load()
        my_art = AsciiArt.from_pillow_image(im)
    my_art.to_html_file(htmlOut,
                        columns=columnsOut,
                        width_ratio=widthRatio,
                        monochrome=True,
                        styles='background-color: black;')

    # Convert HTML to image
    hti = Html2Image()
    hti.screenshot(
        html_file=htmlOut, save_as='ascii.png'
)

    jp.A(text='Link to ASCII art',
         href='/static/' + nameOut,
         target='_blank',
         a=self.out_div,
         classes='m-2 p-2 text-xl text-white bg-blue-500 hover:bg-blue-700')


def image_load(self, msg):
    """Load image and generate preview"""
    print("==== image_load ====")
    self.file_div.delete_components()
    self.image_div.delete_components()
    # First delete any old session dirs
    sessionDir = os.path.abspath(msg.session_id)
    shutil.rmtree(sessionDir)
    # Create new session dir
    os.mkdir(sessionDir)
    
    # Find the element in the form data that contains the file information
    print('===== msg =======')
    print(msg)
    for c in msg.form_data:
        print('===== c =======')
        print(c)
        if c.type == 'file':
            print('===== c.type = file =====')
            print(c)
            break
    # Write the content to a file after decoding the base64 content
    myImages = []
    for i, v in enumerate(c.files):
        _ , fExtension = os.path.splitext(v.name)
        fName = str(uuid.uuid4())
        fPathOut = os.path.abspath(msg.session_id + '/' + fName + fExtension)
        with open(fPathOut, 'wb') as f:
            f.write(base64.b64decode(v.file_content))
            myImages.append(fPathOut)

    for myImage in myImages:
        print("==== myImages loop:")
        print(myImage)
        with Image.open(myImage) as im:
            im.load()
            # Compute sensible width for display
            iHeight = im.height
            iWidth =  im.width
            vRatio = 700/iHeight
            hRatio = 700/iWidth
            ratio  = min(vRatio, hRatio)
            oHeight = round(ratio*iHeight)
            oWidth = round(ratio*iWidth)
            print("Ratio = " + str(ratio))
        
        styleStr = 'width: ' + str(oWidth) + 'px'
        print("=== styleStr: " + styleStr)

        # Internal "static" path used by justpy to render the image
        srcRef = '/static/' + msg.session_id + '/' + os.path.basename(myImage)
        print(srcRef)
        jp.Div(text=myImage, a=self.file_div, classes='font-mono m-1 p-2')

        img1 = jp.Img(src=srcRef,
                      a=self.image_div,
                      style = styleStr)
        print("==== IMAGEELT:")
        print(img1)


def set_columns(self, msg):
    """Set number of columns"""
    global columnsOut
    columnsOut = self.value

def set_widthratio(self, msg):
    """Set width ratio"""
    global widthRatio
    widthRatio = self.value

def createPage():
    """Create web page"""
    global colourFlag

    wp = jp.WebPage()
   
    image_div = jp.Div(classes='m-2 p-2 overflow-auto border-4 flex flex-wrap content-start',
                       style='height: 70vh',
                       a=wp)

    out_div = jp.Div(classes='font-mono m-2 p-2',
                     style='height: 20vh font-size: 6px',
                     a=wp)

    # Upload form
    f1 = jp.Form(enctype='multipart/form-data',
                a=wp,
                style='height: 20vh',
                submit=image_load)
    # Load file
    jp.Label(text='Image',
             classes='font-bold mb-2',
             a=f1)
    in1 = jp.Input(type='file',
                   classes=jp.Styles.input_classes,
                   a=f1,
                   multiple=False,
                   accept='image/*')

    b1 = jp.Button(type='submit',
                   text='Upload',
                   classes=jp.Styles.button_simple,
                   a=f1)

    f1.file_div = jp.Div(a=wp)
    f1.image_div = jp.Div(a=image_div)
    #in1.image_div = jp.Div(a=image_div)

    """
    # Form for other input
    f2 = jp.Form(enctype='multipart/form-data',
                a=wp,
                style='height: 20vh')

    # Set number of columns
    jp.Label(text='Columns',
             classes='font-bold mb-2',
             a=f2)
    in2 = jp.Input(type='number',
                   classes=jp.Styles.input_classes,
                   a=f2,
                   value=columnsOut)
    in2.on('input', set_columns)
    in2.on('change',set_columns)
 
     # Set width ratio
    jp.Label(text='Width ratio',
             classes='font-bold mb-2',
             a=f2)
    in3 = jp.Input(type='number',
                   step='0.1',
                   classes=jp.Styles.input_classes,
                   a=f2,
                   value=widthRatio)
    in3.on('input', set_widthratio)
    in3.on('change',set_widthratio)

    # Toggle between monochrome and colour
    jp.Label(text='Colour output',
             classes='font-bold mb-2',
             a=f2)
    in4 = jp.Input(type='checkbox',
                   classes='m-2 p-2 form-checkbox',
                   a=f2,
                   model=colourFlag)

    b2 = jp.Button(type='submit',
                   text='Asciify',
                   classes=jp.Styles.button_simple,
                   a=f2)
    b2.imageRef = in1.file_div
    b2.on('click', asciifyToFile)
    b2.out_div = jp.Div(a=image_div)
    """

    return wp


def main():
    """Main function"""
    jp.justpy(createPage, websockets=False)


if __name__ == "__main__":
    main()