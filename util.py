from PIL import Image
import io

def convertCvFrame2Bytes(cvFrame):
    stream = convertCvFrame2Stream(cvFrame)
    bin_img = stream.getvalue()
    return bin_img

def convertCvFrame2Stream(cvFrame):
    pil_img = Image.fromarray(cvFrame)
    stream = io.BytesIO()
    pil_img.save(stream, format='JPEG')
    return stream

