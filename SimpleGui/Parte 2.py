import FreeSimpleGUI as sg

layout = [
    [sg.Text('digite um texto')],
    [sg.InputText(key = '-INPUT-')],
    [sg.Button('mostrar valor')]
]
janela = sg.Window('janela',layout)
while True:
    event,values = janela.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'mostrar valor':
        input_text = values['-INPUT-']
        sg.popup(f'seu numero:{input_text}')


janela.close()

