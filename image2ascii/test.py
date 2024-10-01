import justpy as jp

def check_test():
    wp = jp.WebPage(data={'checked': True})
    label = jp.Label(a=wp, classes='m-2 p-2 inline-block')
    c = jp.Input(type='checkbox',
                 classes='m-2 p-2 form-checkbox',
                 a=label,
                 model=[wp, 'checked'])
    caption = jp.Span(text='Monochrome output', a=label)

    in1 = jp.Input(model=[wp, 'checked'], a=wp, classes='border block m-2 p-2')
    return wp

jp.justpy(check_test)
