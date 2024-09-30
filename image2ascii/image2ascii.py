#! /usr/bin/env python3

import os
#from uvicorn import Config
import justpy as jp
from ascii_magic import AsciiArt

__version__ = '0.1.0'

# Set following variable as global as sharing them otherwise within
# Justpy is a major PITA
columnsOut = 150

def asciifyToFile(self, msg):
    """Create ASCII art from file, write result to HTML file and generate link
    to result (which opens in a new browser tab)"""
    global columnsOut
    self.out_div.delete_components()
    imageIn = self.imageRef[0].text
    nameOut = 'ascii.html'
    htmlOut = os.path.abspath(nameOut)
    my_art = AsciiArt.from_image(imageIn)
    my_art.to_html_file(htmlOut,
                        columns=columnsOut,
                        width_ratio=2.2,
                        monochrome=False,
                        styles='background-color: black;')

    jp.A(text='Link to ASCII art',
         href='/static/' + nameOut,
         target='_blank',
         a=self.out_div,
         classes='m-2 p-2 text-xl text-white bg-blue-500 hover:bg-blue-700')


def image_load(self, msg):
    """Load image and generate preview"""
    self.file_div.delete_components()
    self.image_div.delete_components()
    for f in msg.files:
        print(f)
        jp.Div(text=os.path.abspath(f.name), a=self.file_div, classes='font-mono m-1 p-2')
        jp.Img(src='/static/' + f.name, a=self.image_div, style = 'width: 700px')


def set_columns(self, msg):
    """Set number of columns"""
    global columnsOut
    columnsOut = self.value

def createPage():
    """Create web page"""
    wp = jp.WebPage()
    f = jp.Form(enctype='multipart/form-data', a=wp)
    io_div = jp.Div(classes='m-2 p-2 overflow-auto border-4 flex flex-wrap content-start',
                    style='height: 80vh',
                    a=wp)
    image_div = jp.Div(classes='m-1 p-2',
                       style='width: 60vh',
                       a=io_div)
    out_div = jp.Div(classes='font-mono m-1 p-2',
                     style='width: 80vh font-size: 6px background-color: black',
                     a=io_div)
    
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
                   value=150)
    in2.on('input', set_columns)
    in2.on('change',set_columns)
 
    b1 = jp.Button(type='submit',
                   text='Asciify',
                   classes=jp.Styles.button_simple,
                   a=f)
    b1.imageRef = in1.file_div
    b1.on('click', asciifyToFile)
    b1.out_div = jp.Div(a=out_div)

    return wp


def main():
    """Main function"""
    #config = Config('justpy.env')
    #STATIC_DIRECTORY = config('STATIC_DIRECTORY', cast=str, default=os.getcwd())
    jp.justpy(createPage)


if __name__ == "__main__":
    main()