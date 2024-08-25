# convert base64 to image 
import base64
import pathlib

current_path = str(pathlib.Path(__file__).parent.resolve())
image = open(current_path + '/yehchitsai.jpg', 'rb')
image_read = image.read()
image_64_encode = base64.encodebytes(image_read)
# print(image_64_encode)
image_encode_file = open(f'{current_path}/base64.txt','w')
image_encode_file.write(str(image_64_encode))
image_encode_file.close()

