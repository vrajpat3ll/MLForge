import cv2 as cv
import random as rand

def interpolation_method():
    methods = [
        cv.INTER_AREA,
        cv.INTER_LINEAR,
        cv.INTER_LANCZOS4,
        cv.INTER_CUBIC,
        cv.INTER_NEAREST,
    ]
    return methods[(rand.randint(0, len(methods) - 1))]
    
def up_sample(img_path:str):
    """up sample the image based on various interpolation methods

    Args:
        img_path (str): path to the image
    """
    try:
        image = cv.imread(img_path)
    except Exception as e:
        print(e)
    image = cv.resize(image, dsize=(2040, 2040), interpolation=interpolation_method())
    return image


if __name__ == '__main__':
    import os
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    LR_dir = os.path.join(os.path.dirname(__file__), 'HR')
    
    for i in range(1, 901):
        read_img_number = f'{str(i).zfill(4)}.png'
        img_file = os.path.join(data_dir, read_img_number)
        image = up_sample(img_file)
        img_number = f'{str(i).zfill(4)}.png'

        if not cv.imwrite(os.path.join(LR_dir, img_number), image):
            print(f"There was some error writing this file: {img_number}")
        print(f"{img_number} saved to HR/", end='\r')