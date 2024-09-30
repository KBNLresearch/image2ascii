#! /usr/bin/env python3

import os
#from uvicorn import Config
import justpy as jp
from ascii_magic import AsciiArt

__version__ = '0.1.0'

columnsOut = 150

def asciifyToFile(self, msg):
    #columnsOut = self.columns[0].text
    global columnsOut
    print("asciifyToFile")
    print("COLUMNS (receiving): " + str(columnsOut))
 
def set_columns(self, msg):
    """Set number of columns"""
    global columnsOut
    columnsOut = self.value
    print("Columns: " + str(columnsOut))
    #self.columns_div.delete_components()
    #jp.Div(text=self.value, a=self)

def createPage():
    """Create web page"""
    wp = jp.WebPage()
    f = jp.Form(enctype='multipart/form-data', a=wp)

    # Set number of columns 
    in2 = jp.Input(type='number',
                   classes=jp.Styles.input_classes,
                   a=f,
                   value=columnsOut)
    in2.on('input', set_columns)
    in2.on('change',set_columns)

    #in2.columns_div = jp.Div(a=wp)
    #in2.columns = None
    print("Columns (main): " + str(columnsOut))
 

    b1 = jp.Button(type='submit',
                   text='Asciify',
                   classes=jp.Styles.button_simple,
                   a=f)
    b1.on('click', asciifyToFile)

    return wp


def main():
    """Main function"""
    #config = Config('justpy.env')
    #STATIC_DIRECTORY = config('STATIC_DIRECTORY', cast=str, default=os.getcwd())
    jp.justpy(createPage)


if __name__ == "__main__":
    main()