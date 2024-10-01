#! /usr/bin/env python3

import os
import base64
import logging
#from uvicorn import Config
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
    self.file_div.delete_components()
    self.image_div.delete_components()

    """
    # If directory for session does not exist, create one
    # The name of the directory is the session_id
    if not os.path.isdir(msg.session_id):
        os.mkdir(msg.session_id)
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
    #for i, v in enumerate(c.files):
    for f in msg.files:
        print(type(f))
        print('=============')
        print(f)

        #with open(f'{msg.session_id}/{v.name}', 'wb') as f:
        #    f.write(base64.b64decode(v.file_content))
    """
    for f in msg.files:
        fPath = os.path.abspath(f.name)
        with Image.open(fPath) as im:
            # Compute sensible width for display
            iHeight = im.height
            iWidth =  im.width
            vRatio = 700/iHeight
            hRatio = 700/iWidth
            ratio  = min(vRatio, hRatio)
            oHeight = round(ratio*iHeight)
            oWidth = round(ratio*iWidth)
        
        styleStr = 'width: ' + str(oWidth) + 'px'

        jp.Div(text=fPath, a=self.file_div, classes='font-mono m-1 p-2')
        jp.Img(src='/static/' + f.name, a=self.image_div, style = styleStr)

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

    #io_div = jp.Div(classes='m-2 p-2 overflow-auto border-4 flex flex-wrap content-start',
    #                style='width: 80 vw height: 100vh',
    #                a=wp)
    
    image_div = jp.Div(classes='m-2 p-2 overflow-auto border-4 flex flex-wrap content-start',
                       style='height: 70vh',
                       a=wp)

    out_div = jp.Div(classes='font-mono m-2 p-2',
                     style='height: 20vh font-size: 6px',
                     a=wp)

    f = jp.Form(enctype='multipart/form-data',
                a=wp,
                style='height: 20vh')
    # Load file
    jp.Label(text='Image',
             classes='font-bold mb-2',
             a=f)
    in1 = jp.Input(type='file',
                   classes=jp.Styles.input_classes,
                   a=f,
                   multiple=False,
                   accept='image/*')
    
    in1.file_div = jp.Div(a=wp)
    in1.image_div = jp.Div(a=image_div)
    in1.on('input', image_load)
    in1.on('change', image_load)

    # Set number of columns
    jp.Label(text='Columns',
             classes='font-bold mb-2',
             a=f)
    in2 = jp.Input(type='number',
                   classes=jp.Styles.input_classes,
                   a=f,
                   value=columnsOut)
    in2.on('input', set_columns)
    in2.on('change',set_columns)
 
     # Set width ratio
    jp.Label(text='Width ratio',
             classes='font-bold mb-2',
             a=f)
    in3 = jp.Input(type='number',
                   step='0.1',
                   classes=jp.Styles.input_classes,
                   a=f,
                   value=widthRatio)
    in3.on('input', set_widthratio)
    in3.on('change',set_widthratio)

    """
    # Toggle between monochrome and colour
    jp.Label(text='Colour output',
             classes='font-bold mb-2',
             a=f)
    in4 = jp.Input(type='checkbox',
                   classes='m-2 p-2 form-checkbox',
                   a=f,
                   model=colourFlag)
    """
    b1 = jp.Button(type='submit',
                   text='Asciify',
                   classes=jp.Styles.button_simple,
                   a=f)
    b1.imageRef = in1.file_div
    b1.on('click', asciifyToFile)
    b1.out_div = jp.Div(a=image_div)

    return wp


def main():
    """Main function"""
    jp.justpy(createPage, websockets=False)


if __name__ == "__main__":
    main()