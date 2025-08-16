import FreeSimpleGUI as sg
from PIL import Image
import io
def resize_image(image_path):
    img = Image.open(image_path)
    img = img.resize((800,600),Image.Resampling.LANCZOS)
    return img


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
            resized_image = resize_image(file_path)
            img_bytes = io.BytesIO()
            resized_image.save(img_bytes,format='PNG')
            janela["-IMAGE-"].update(data=img_bytes.getvalue())
    elif event =='sobre':
        sg.popup("ola foi desenvolvido pelo vampeta")        

janela.close()

#tem que ter sobre a imagem salvar e o sobre é da original