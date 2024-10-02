#! /usr/bin/env python3

import os
import glob
import uuid
import base64
import time
import justpy as jp
from ascii_magic import AsciiArt, Front, Back
from html2image import Html2Image
from PIL import Image

__version__ = '0.1.0'

# Set following variables as global as sharing them otherwise within
# Justpy is a major PITA!
columnsOut = 400
widthRatio = 2.2

def asciifyToFile(self, msg):
    """Create ASCII art from file, write result to HTML file and generate link
    to result (which opens in a new browser tab)"""
    global columnsOut
    global widthRatio
    self.out_div.delete_components()
    imageIn = os.path.abspath(self.imageRef[0].text)
    nameOut = 'ascii.html'
    htmlOut = os.path.abspath(nameOut)
    txtOut = os.path.abspath('ascii.txt')

    with Image.open(imageIn) as im:
        im.load()
        my_art = AsciiArt.from_pillow_image(im)
    my_art.to_html_file(htmlOut,
                        columns=columnsOut,
                        width_ratio=widthRatio,
                        monochrome=True,
                        styles='background-color: black;'
                        )

    ## TEST output to text file
    my_art.to_file(txtOut,
                   columns=columnsOut,
                   width_ratio=widthRatio,
                   monochrome=True)

    # Convert HTML to image
    #hti = Html2Image()
    #hti.screenshot(
    #    html_file=htmlOut, save_as='ascii.png')

    jp.A(text='Link to ASCII art',
         href='/static/' + nameOut,
         target='_blank',
         a=self.out_div,
         classes='m-2 p-2 text-xl text-white bg-blue-500 hover:bg-blue-700')


def image_load(self, msg):
    """Load image and generate preview"""
    self.file_div.delete_components()
    self.image_div.delete_components()

    # Session dir (used to store copy of uploaded image)
    sessionDir = os.path.abspath(msg.session_id)

    # Create new session dir if it doesn't exist
    if not os.path.isdir(sessionDir):
        os.mkdir(sessionDir)

    # Delete contents of session dir
    if os.path.isdir(sessionDir):
        filesSd = glob.glob(sessionDir + '/*')
        for f in filesSd:
            os.remove(f)
    
    # Find the element in the form data that contains the file information
    for c in msg.form_data:
        print(c)
        if c.type == 'file':
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

    # Maximum image display dimensions (in pixels)
    maxHeight = 550
    maxWidth = 800
    for myImage in myImages:
        with Image.open(myImage) as im:
            im.load()
            # Compute sensible width for display
            iHeight = im.height
            iWidth =  im.width
            vRatio = maxHeight/iHeight
            hRatio = maxWidth/iWidth
            ratio  = min(vRatio, hRatio)
            oHeight = round(ratio*iHeight)
            oWidth = round(ratio*iWidth)
            print("Ratio = " + str(ratio))
        
        styleStr = 'width: ' + str(oWidth) + 'px'

        ## TEST
        debugStr = 'width: ' + str(oWidth) + '; height: ' + str(oHeight)

        # Internal "static" path used by justpy to render the image
        srcRef = '/static/' + msg.session_id + '/' + os.path.basename(myImage)
        jp.Div(text=debugStr, a=self.file_div, classes='font-mono m-1 p-2')

        img1 = jp.Img(src=srcRef,
                      a=self.image_div,
                      style = styleStr)

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

    wp = jp.WebPage()
   
    image_div = jp.Div(classes='m-2 p-2  border-4 flex flex-wrap content-start',
                       style='display: block; margin: 0 auto; max-height: 100%; max-width: 100%',
                       a=wp)

    form1_div = jp.Div(a=wp,
                       classes='m-2 p-2 overflow-auto flex flex-wrap content-start')

    form2_div = jp.Div(a=wp,
                       classes='m-2 p-2 overflow-auto flex flex-wrap content-start')

    form3_div = jp.Div(a=wp,
                       classes='m-2 p-2 overflow-auto flex flex-wrap content-start')

    # Upload form
    f1 = jp.Form(enctype='multipart/form-data',
                a=form1_div,
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

    # Form for other input
    f2 = jp.Form(enctype='multipart/form-data',
                a=form2_div)

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
                   
    b2 = jp.Button(type='submit',
                   text='Generate Ascii!',
                   classes=jp.Styles.button_simple,
                   a=f2)
    b2.imageRef = f1.file_div
    b2.on('click', asciifyToFile)

    asciiLinkDiv = jp.Div(a=form3_div,
                          classes='m-2 p-2 overflow-auto flex flex-wrap content-start')

    b2.out_div = jp.Div(a=asciiLinkDiv)

    return wp


def main():
    """Main function"""
    jp.justpy(createPage, websockets=False)


if __name__ == "__main__":
    main()