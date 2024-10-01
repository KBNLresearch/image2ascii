import justpy as jp
import base64
import os
from PIL import Image


def image_loadOld(self, msg):
    # If directory for session does not exist, create one
    # The name of the directory is the session_id
    if not os.path.isdir(msg.session_id):
        os.mkdir(msg.session_id)
    # Find the element in the form data that contains the file information
    for c in msg.form_data:
        if c.type == 'file':
            break
    # Write the content to a file after decoding the base64 content
    for i, v in enumerate(c.files):
        with open(f'{msg.session_id}/{v.name}', 'wb') as f:
            f.write(base64.b64decode(v.file_content))
    file_list = os.listdir(msg.session_id)
    self.image_div.delete_components()
    if file_list:
        for file in file_list:
            ThumbNail(pic_file=f'/static/{msg.session_id}/{file}', a=self.image_div)
    else:
        jp.Div(text='No images uploaded yet', a=self.image_div, classes='text-3xl')

def image_loadTest(self, msg):
    print("Submitted!")

def image_load(self, msg):
    """Load image and generate preview"""
    print("==== image_load ====")

    # If directory for session does not exist, create one
    # The name of the directory is the session_id
    if not os.path.isdir(msg.session_id):
        os.mkdir(msg.session_id)
    # Find the element in the form data that contains the file information
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
        fName, fExtension = os.path.splitext(v.name)
        fNameOut = 'image' + fExtension
        with open(f'{msg.session_id}/{fNameOut}', 'wb') as f:
            f.write(base64.b64decode(v.file_content))
            myImages.append(fNameOut)

    for myImage in myImages:
        fPath = os.path.abspath(myImage)
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
        jp.Img(src='/static/' + msg.session_id + '/' + myImage,
               a=self.image_div,
               style = styleStr)


def upload_test(request):
    wp = jp.WebPage()
    image_div = jp.Div(classes='m-2 p-2 overflow-auto border-4 flex flex-wrap content-start',
                       style='height: 70vh',
                       a=wp)

    f1 = jp.Form(a=wp, enctype='multipart/form-data' , submit=image_load)
    f1.image_div = image_div  # Will be used in submit event handler
    jp.Input(type='file', classes=jp.Styles.input_classes, a=f1, multiple=False, accept='image/*')
    jp.Button(type='submit', text='Upload', classes=jp.Styles.button_simple, a=f1)
    return wp

jp.justpy(upload_test, websockets=False)