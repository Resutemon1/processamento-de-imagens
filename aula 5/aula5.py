import FreeSimpleGUI as sg
from PIL import Image, ExifTags,ImageFilter,ImageDraw
import io
import os
import webbrowser
import requests

image_atual = None
image_path = None
image_anterior = None
changes_stack = []
def url_download(url):
    global image_atual
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            image_atual = Image.open(io.BytesIO(r.content))
            show_image()
        else:
            sg.popup("Falha ao baixar a imagem. Verifique a URL e tente novamente.")
    except Exception as e:
        sg.popup(f"Erro ao baixar a imagem: {str(e)}")

def show_image():
    global image_atual
    try:
        resized_img = resize_image(image_atual)
        img_bytes = io.BytesIO()
        resized_img.save(img_bytes, format='PNG')
        window['-IMAGE-'].update(data=img_bytes.getvalue())
    except Exception as e:
        sg.popup(f"Erro ao exibir a imagem: {str(e)}")

def save_last_state():
  global image_atual, image_anterior
  if image_atual:
    image_anterior = image_atual.copy()
    changes_stack.append(image_anterior)

def load_last_state():
  global image_atual, image_anterior
  if image_atual and len(changes_stack) > 0:
    image_atual = changes_stack.pop()
    show_image()

def resize_image(img):
    try:
        img = img.resize((800, 600), Image.Resampling.LANCZOS) 
        return img
    except Exception as e:
        sg.popup(f"Erro ao redimensionar a imagem: {str(e)}")

def open_image(filename):
    global image_atual
    global image_path
    try:
        image_path = filename
        image_atual = Image.open(filename)    
        show_image()
    except Exception as e:
        sg.popup(f"Erro ao abrir a imagem: {str(e)}")

def save_image(filename):
    global image_atual
    try:
        if image_atual:
            with open(filename, 'wb') as file:
                image_atual.save(file)
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao salvar a imagem: {str(e)}")

def info_image():
    global image_atual
    global image_path
    try:
        if image_atual:
            save_last_state()
            largura, altura = image_atual.size
            formato = image_atual.format
            tamanho_bytes = os.path.getsize(image_path)
            tamanho_mb = tamanho_bytes / (1024 * 1024)
            sg.popup(f"Tamanho: {largura} x {altura}\nFormato: {formato}\nTamanho em MB: {tamanho_mb:.2f}")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao exibir informações da imagem: {str(e)}")

def negativo():
    global image_atual
    global image_anterior
    try:
        if image_atual:
            save_last_state()
            imgtemp = image_atual.load()
            largura, altura = image_atual.size
            for  i in range (largura):
                for j in range (altura):
                   r,g,b =  image_atual.getpixel((i,j))
                   rNovo = 255-r
                   gNovo = 255-g
                   bNovo = 255-b
                   imgtemp[i,j] = (rNovo,gNovo,bNovo)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao exibir informações da imagem: {str(e)}")
def fourBits():
    global image_atual
    global image_anterior
    bits = sg.popup_get_text("digite a quantidade de bits(1 a 32):", default_text = "4")
    try:
        bits = int(bits)
        bits = max(1,min(32,bits))
    except ValueError:
        sg.popup("por favor, insira um valor numero valido")
    try:
        if image_atual:
            save_last_state()
            imgtemp = image_atual.load()
            largura, altura = image_atual.size
            image_atual = image_atual.convert("P", palette = Image.ADAPTIVE, colors = bits)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao exibir informações da imagem: {str(e)}")
def vermelho():
    global image_atual
    global image_anterior
    try:
        if image_atual:
            save_last_state()
            imgtemp = image_atual.load()
            largura, altura = image_atual.size
            for  i in range (largura):
                for j in range (altura):
                   r,g,b =  image_atual.getpixel((i,j))
                   rNovo = r
                   gNovo = 0
                   bNovo = 0
                   imgtemp[i,j] = (rNovo,gNovo,bNovo)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao exibir informações da imagem: {str(e)}")
def pretoBranco():
    global image_atual
    global image_anterior
    try:
        if image_atual:
            save_last_state()
            imgtemp = image_atual.load()
            largura, altura = image_atual.size
            for  i in range (largura):
                for j in range (altura):
                   rgb =  image_atual.getpixel((i,j))
                   rNovo = int(rgb[0] * 0.3)
                   gNovo = int(rgb[1] * 0.59)
                   bNovo = int(rgb[2] * 0.11)
                   rfinal = rNovo+gNovo+bNovo
                   gfinal = rfinal
                   bfinal = rfinal

                   imgtemp[i,j] = (rfinal,gfinal,bfinal)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao exibir informações da imagem: {str(e)}")  
def blur():
    global image_atual
    global image_anterior
    radius = sg.popup_get_text("digite a quantidade de Blur(0 a 20):", default_text = "2")
    try:
        radius = int(radius)
        radius = max(0,min(20,radius))
    except ValueError:
        sg.popup("por favor, insira um valor numero valido")    
    try:
        if image_atual:
            save_last_state()
            imgtemp = image_atual.load()
            image_atual = image_atual.filter(ImageFilter.GaussianBlur(radius))
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao exibir informações da imagem: {str(e)}")              

def sepia():
    global image_atual
    global image_anterior
    try:
        if image_atual:
            save_last_state()
            imgtemp = image_atual.load()
            largura, altura = image_atual.size
            for  i in range (largura):
                for j in range (altura):
                   r,g,b =  image_atual.getpixel((i,j))
                   rNovo = r + 150

                   if rNovo>255:
                      rNovo = 255

                   gNovo = r + 100

                   if gNovo>255:
                      gNovo = 255
                   bNovo = r + 50

                   if bNovo>255:
                     bNovo = 255                   
                   imgtemp[i,j] = (rNovo,gNovo,bNovo)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao exibir informações da imagem: {str(e)}")

def exif_data():
    global image_atual
    try:
        if image_atual:
            exif = image_atual._getexif() 
            if exif:
                exif_data = ""
                for tag, value in exif.items():
                    if tag in ExifTags.TAGS:
                        if tag == 37500 or tag == 34853: #Remove os dados customizados (37500) e de GPS (34853)
                            continue
                        tag_name = ExifTags.TAGS[tag]
                        exif_data += f"{tag_name}: {value}\n"
                sg.popup("Dados EXIF:", exif_data)
            else:
                sg.popup("A imagem não possui dados EXIF.")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao ler dados EXIF: {str(e)}")
def rotate_image(degrees):
    global image_atual
    global previous_state
    try:
        if image_atual:
            save_last_state()
            image_atual = image_atual.rotate(degrees, expand=True)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao girar a imagem: {str(e)}")
def apply_contour_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            save_last_state()
            image_atual = image_atual.filter(ImageFilter.CONTOUR)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de contorno: {str(e)}")
def apply_detail_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            save_last_state()
            image_atual = image_atual.filter(ImageFilter.DETAIL)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de detalhe: {str(e)}") 
def apply_edge_enhance_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            save_last_state()
            image_atual = image_atual.filter(ImageFilter.EDGE_ENHANCE)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de realce de bordas: {str(e)}")
def apply_emboss_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            save_last_state()
            image_atual = image_atual.filter(ImageFilter.EMBOSS)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de relevo: {str(e)}")
def apply_find_edges_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            save_last_state()
            image_atual = image_atual.filter(ImageFilter.FIND_EDGES)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de detectar bordas: {str(e)}")

def apply_sharpen_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            save_last_state()
            image_atual = image_atual.filter(ImageFilter.SHARPEN)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de nitidez: {str(e)}")

def apply_smooth_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            save_last_state()
            image_atual = image_atual.filter(ImageFilter.SMOOTH)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de suavizar: {str(e)}")

def apply_minfilter_filter():
    global image_atual
    global previous_state

    size = sg.popup_get_text("Digite a quantidade de filtro (3 a 20):", default_text="3")
    try:
        size = int(size)
        size = max(3, min(20, size))
    except ValueError:
        sg.popup("Por favor, insira um valor numérico válido.")
        return

    try:
        if image_atual:
            save_last_state()
            image_atual = image_atual.filter(ImageFilter.MinFilter(size=size))
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro mínimo: {str(e)}")

def apply_maxfilter_filter():
    global image_atual
    global previous_state

    size = sg.popup_get_text("Digite a quantidade de filtro (3 a 20):", default_text="3")
    try:
        size = int(size)
        size = max(3, min(20, size))
    except ValueError:
        sg.popup("Por favor, insira um valor numérico válido.")
        return

    try:
        if image_atual:
            save_last_state()
            image_atual = image_atual.filter(ImageFilter.MaxFilter(size=size))
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro máximo: {str(e)}")               
def gps_data():
    global image_atual
    try:
        if image_atual:
            exif = image_atual._getexif()
            if exif:
                gps_info = exif.get(34853)  #Tag para informações de GPS
                print (gps_info[1], gps_info[3])
                if gps_info:
                    latitude = int(gps_info[2][0]) + int(gps_info[2][1]) / 60 + int(gps_info[2][2]) / 3600
                    if gps_info[1] == 'S':  #Verifica se a direção é 'S' (sul)
                        latitude = -latitude
                    longitude = int(gps_info[4][0]) + int(gps_info[4][1]) / 60 + int(gps_info[4][2]) / 3600
                    if gps_info[3] == 'W':  #Verifica se a direção é 'W' (oeste)
                        longitude = -longitude
                    sg.popup(f"Latitude: {latitude:.6f}\nLongitude: {longitude:.6f}")
                    open_in_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
                    if sg.popup_yes_no("Deseja abrir no Google Maps?") == "Yes":
                        webbrowser.open(open_in_maps_url)
                else:
                    sg.popup("A imagem não possui informações de GPS.")
            else:
                sg.popup("A imagem não possui dados EXIF.")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao ler dados de GPS: {str(e)}")
def show_histogram_rgb():
    global image_atual
    try:
        if not image_atual:
            sg.popup("Nenhuma imagem aberta.")
            return

        #Garante que a imagem em RGB
        img_rgb = image_atual.convert('RGB')
        hist = img_rgb.histogram()

        r = hist[0:256]
        g = hist[256:512]
        b = hist[512:768]

        #Normaliza para caber na altura do gráfico
        width, height = 256, 200
        margin = 10
        max_count = max(max(r), max(g), max(b), 1)

        hist_img = Image.new('RGB', (width, height), 'black')
        draw = ImageDraw.Draw(hist_img)

        for x in range(256):
            rh = int((r[x] / max_count) * (height - margin))
            gh = int((g[x] / max_count) * (height - margin))
            bh = int((b[x] / max_count) * (height - margin))

            #Desenha linhas verticais sobrepostas para cada canal
            draw.line([(x, height - 1), (x, height - 1 - rh)], fill=(255, 0, 0))
            draw.line([(x, height - 1), (x, height - 1 - gh)], fill=(0, 255, 0))
            draw.line([(x, height - 1), (x, height - 1 - bh)], fill=(0, 0, 255))

        #Amplia para melhor visualização mantendo aspecto
        scale_x, scale_y = 3, 2
        hist_big = hist_img.resize((width * scale_x, height * scale_y), Image.LANCZOS)

        img_bytes = io.BytesIO()
        hist_big.save(img_bytes, format='PNG')

        layout = [
            [sg.Image(data=img_bytes.getvalue(), key='-HIST-')],
            [sg.Button('Fechar')]
        ]
        win_hist = sg.Window('Histograma RGB', layout, modal=True, finalize=True)
        while True:
            e, _ = win_hist.read()
            if e in (sg.WINDOW_CLOSED, 'Fechar'):
                break
        win_hist.close()
    except Exception as e:
        sg.popup(f"Erro ao gerar histograma: {str(e)}")
layout = [
    [sg.Menu([
            ['Arquivo',
                 ['Abrir',
                  'Abrir URL',
                   'Salvar',
                    'Fechar']],
            ['EXIF',
                ['Mostrar dados da imagem',
                 'Mostrar dados de GPS']], 
            ['Sobre a image', ['Informacoes']], 
            ['imagem',[
                'girar',
                    ['gira 90 graus a direita',
                    'gira 90 graus a esquerda'],
                'histograma rgb',
                'filtros',
                    ['negativo',
                    'sepia',
                    'vermelho',
                    'preto-branco',
                    'bits',
                    'blur',
                    'contorno',
                    'detalhe',
                    'realce de bordas',
                    'Relevo',
                    'detectar bordas',
                    'nitidez',
                    'suavizar',
                    'filtro minimo',
                    'filtro maximo',
                    'desfazer']]],
            ['Sobre',
                 ['Desenvolvedor']]
        ])],
    [sg.Image(key='-IMAGE-', size=(800, 600))],
]

window = sg.Window('Photo Shoping', layout, finalize=True)

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Fechar'):
        break
    elif event == 'Abrir':
        arquivo = sg.popup_get_file('Selecionar image', file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
        if arquivo:
            open_image(arquivo)
    elif event == 'Abrir URL':
        url = sg.popup_get_text("Digite a url")
        if url:
            url_download(url)
    elif event == 'Salvar':
        if image_atual:
            arquivo = sg.popup_get_file('Salvar image como', save_as=True, file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
            if arquivo:
                save_image(arquivo)
    elif event == 'Informacoes':
        info_image()
    elif event == 'Mostrar dados da imagem':
        exif_data()
    elif event == 'Mostrar dados de GPS':
        gps_data()
    elif event == 'Desenvolvedor':
        sg.popup('Desenvolvido por caio - BCC 6º Semestre')
    elif event == 'negativo':
        negativo()
    elif event == 'desfazer':
        load_last_state()
    elif event == 'sepia':
        sepia()
    elif event == 'vermelho':
        vermelho()
    elif event == 'preto-branco':
        pretoBranco()
    elif event == 'bits':
        fourBits()   
    elif event == 'blur':
        blur()
    elif event =='gira 90 graus a direita':
        rotate_image(-90)
    elif event =='gira 90 graus a esquerda':    
        rotate_image(90)
    elif event == 'contorno':
        apply_contour_filter()
    elif event == 'detalhe':
        apply_detail_filter()
    elif event =='realce de bordas':
        apply_edge_enhance_filter()
    elif event == 'Relevo':
        apply_emboss_filter()
    elif event == 'detectar bordas':
        apply_find_edges_filter()
    elif event == 'nitidez':
        apply_sharpen_filter()
    elif event == 'suavizar':
        apply_smooth_filter()
    elif event == 'filtro minimo':
        apply_minfilter_filter()
    elif event == 'filtro maximo':
        apply_maxfilter_filter()
    elif event == 'histograma rgb':
        show_histogram_rgb()
window.close()