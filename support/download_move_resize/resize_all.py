import os
import sys
import numpy as np
import pandas as pd
from PIL import Image
from PIL import ImageFile

Image.MAX_IMAGE_PIXELS = 999000000
ImageFile.LOAD_TRUNCATED_IMAGES = True

def pure_pil_alpha_to_color_v2(image, color=(255, 255, 255)):
    """Alpha composite an RGBA Image with a specified color.

    Simpler, faster version than the solutions above.

    Source: http://stackoverflow.com/a/9459208/284318

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """
    image.load()  # needed for split()
    background = Image.new('RGB', image.size, color)
    background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
    return background

def alpha_composite(front, back):
    """Alpha composite two RGBA images.

    Source: http://stackoverflow.com/a/9166671/284318

    Keyword Arguments:
    front -- PIL RGBA Image object
    back -- PIL RGBA Image object

    """
    front = np.asarray(front)
    back = np.asarray(back)
    result = np.empty(front.shape, dtype='float')
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    falpha = front[alpha] / 255.0
    balpha = back[alpha] / 255.0
    result[alpha] = falpha + balpha * (1 - falpha)
    old_setting = np.seterr(invalid='ignore')
    result[rgb] = (front[rgb] * falpha + back[rgb] * balpha * (1 - falpha)) / result[alpha]
    np.seterr(**old_setting)
    result[alpha] *= 255
    np.clip(result, 0, 255)
    # astype('uint8') maps np.nan and np.inf to 0
    result = result.astype('uint8')
    result = Image.fromarray(result, 'RGBA')
    return result


def alpha_composite_with_color(image, color=(255, 255, 255)):
    """Alpha composite an RGBA image with a single color image of the
    specified color and the same size as the original image.

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """
    back = Image.new('RGBA', size=image.size, color=color + (255,))
    return alpha_composite(image, back)

def resize_image(log, dir, min_size=256):
    
    img = Image.open(os.path.join('original', dir))
    has_transparency = img.info.get('transparency') is not None

    print(dir, img.mode, has_transparency)
    
    try:
        # https://pillow.readthedocs.io/en/latest/_modules/PIL/Image.html
        if has_transparency:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            img = pure_pil_alpha_to_color_v2(img)
        if img.mode != 'RGB':
            img = img.convert('RGB')
    except:
        print('File {} had problems when reading and writing.\n'.format(dir))
        log.write('File {} had problems when reading and writing.\n'.format(dir))
    
    width, height = img.size
    if width >= height:
        short_size = height
    else:
        short_size = width
        
    ratio = min_size / short_size
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    
    img = img.resize([new_width, new_height], Image.ANTIALIAS)

    base_path, file_name = dir.split('/')
    os.makedirs(os.path.join('min{}'.format(min_size), base_path), exist_ok=True)
    file_name, ext = file_name.split('.')
        
    img.save(os.path.join(
        'min{}'.format(min_size), base_path, '{}.jpg'.format(file_name)
    ))
        
    log.write('{},{},{},{},{},{}\n'.format(dir, width, height, new_width, new_height, has_transparency))


def main():

    with open('log_resize.txt', 'a', buffering=1) as log:
        with open(sys.argv[1], 'r') as myfile:
            files = myfile.read().splitlines()
            for f in files:
                f = os.path.normpath(f)
                #print(f)
                mypath = f.split('/', 1)[1]
                #print(mypath)
                resize_image(log, mypath) 

main()
