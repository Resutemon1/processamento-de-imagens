import FreeSimpleGUI as sg
import PIL as 
layout = [
    [sg.Menu([['Arquivo',['Abrir','fechar']],['ajuda',['sobre']]])],
    [sg.Image(key='-IMAGE-',size=(800,600)),]
]
janela = sg.Window('menu foto',layout,resizable=True)
while True:
    event,values = janela.read()
    if event == sg.WINDOW_CLOSED or event =='fechar':
        break
    elif event == 'Abrir':
        file_path = sg.popup_get_file('selecione uma imagem',file_types=(("imagens","*.jpg *.png"),))
        if file_path:
            janela["-IMAGE-"].update(filename = file_path)
    elif event =='sobre':
        sg.popup("ola foi desenvolvido pelo vampeta")        

janela.close()

