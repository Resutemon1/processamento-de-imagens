from PIL import Image,ImageChops
imagem = Image.open("vampeta.jpg")
imagem2 = Image.open("macaco.jpg")
print(imagem.size)
width,height = imagem.size
print(width)
print(height)
print(imagem.filename)
print(imagem.format)
print(imagem.format_description)

#vampeta E Homem macaco
#imagemDupla = ImageChops.add(imagem,imagem2,1)
#imagemDupla.show()