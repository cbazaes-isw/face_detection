from PIL import Image
import io

def convertCvFrame2Bytes(cvFrame):
    pil_img = Image.fromarray(cvFrame)
    stream = io.BytesIO()
    pil_img.save(stream, format='JPEG')
    bin_img = stream.getvalue()
    return bin_img

