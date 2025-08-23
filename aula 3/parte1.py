import FreeSimpleGUI as sg
from PIL import Image
from PIL.ExifTags import TAGS ,GPS
import io
import webbrowser
imgResize = None
imgOriginal = None
latitude = 0.0
longitude = 0.0
altitude = 0.0
def resize_image(image_path):
    global imgResize 
    global imgOriginal 
    img = Image.open(image_path)
    imgOriginal = img
    imgResize = img.resize((800,600),Image.Resampling.LANCZOS)
    

def decimal_coords(coords, ref):
    decimal_degrees = float(coords[0])+ float(coords[1]) / 60 + float(coords[2])/3600
    if ref =="S" or ref =="W":
         decimal_degrees = -1*decimal_degrees
    return decimal_degrees
layout = [
    [sg.Menu([['Arquivo',['Abrir','fechar','salvar como']],['ajuda',['sobre']],['Imagem',['sobreImagem','propriedade','gps','googlemaps']]])],
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
            img_bytes = io.BytesIO()
            resize_image(file_path)
            imgResize.save(img_bytes,format='PNG')
            janela["-IMAGE-"].update(data=img_bytes.getvalue())
    elif event =='sobre':
        sg.popup("ola foi desenvolvido pelo vampeta")        
    elif event == 'sobreImagem':
        if imgOriginal is  None:
            sg.popup('erro: imagem nao carregada')
            continue
        width,height = imgOriginal.size
        format = imgOriginal.format
        sg.popup(f"largura:{width} \naltura:{height}\nformato:{format}")
    elif event =='propriedade':
        if imgOriginal is  None:
            sg.popup('erro: imagem nao carregada')
            continue
        propriedade = imgResize.getexif()
        dados = ""
        for tag_id,value in propriedade.items():
            tag =TAGS.get(tag_id,tag_id)
            if(tag=="GPSInfo"):
                gps = tag_id
            dados+= f"{tag}: {value}\n"
        sg.popup(f"{dados}")

    elif event == 'gps':
        if imgOriginal is  None:
            sg.popup('erro: imagem nao carregada')
            continue
        propriedade = imgResize.getexif()
        gps = ""
        for tag_id,value in propriedade.items():
            tag =TAGS.get(tag_id,tag_id)
            if(tag=="GPSInfo"):
                gps = tag_id
        gpsinfo = propriedade.get_ifd(gps)
        latitude = decimal_coords(gpsinfo[2],gpsinfo[1])
        longitude = decimal_coords(gpsinfo[4],gpsinfo[3])
        altitude = gpsinfo[6]
        sg.popup(f"latitude:{latitude}\nlongitude:{longitude}\naltitude:{altitude}")
    elif event =='googlemaps':
        if imgOriginal is  None:
            sg.popup('erro: imagem nao carregada')
            continue
        propriedade = imgResize.getexif()
        gps = ""
        for tag_id,value in propriedade.items():
            tag =TAGS.get(tag_id,tag_id)
            if(tag=="GPSInfo"):
                gps = tag_id
        gpsinfo = propriedade.get_ifd(gps)
        latitude = decimal_coords(gpsinfo[2],gpsinfo[1])
        longitude = decimal_coords(gpsinfo[4],gpsinfo[3])
        altitude = gpsinfo[6]
        webbrowser.open(f"https://www.google.com/maps?q={latitude},{longitude}")
    elif event =='salvar como':
        filename = sg.popup_get_file('Save file as...', save_as=True, no_window=True,file_types=(('png', '*.png'), ('All Files', '*.*')),initial_folder='.')
        if filename:
            try:
                sg.popup_ok(f"arquivo salvo com sucesso {filename}")
            except Exception as e:
                sg.popup_error(f"Erro ao salvar: {e}")

#tem que ter sobre a imagem salvar e o sobre é da original