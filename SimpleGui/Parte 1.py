import FreeSimpleGUI as sg

layout = [
    [sg.Text('olá')],
    [sg.Button('ok')]
]
janela = sg.Window('janela',layout)
while True:
    event,values = janela.read()
    if event == sg.WINDOW_CLOSED or event ==  'ok':
        break

janela.close

