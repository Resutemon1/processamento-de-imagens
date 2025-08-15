from PIL import Image
imagem = Image.open("vampeta.jpg")
imagem.show()
print(imagem.size)
width,height = imagem.size
print(width)
print(height)
print(imagem.filename)
print(imagem.format)
print(imagem.format_description)
