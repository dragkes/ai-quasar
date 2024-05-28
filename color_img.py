import os
import sys
import torch
import numpy as np
from PIL import Image
from skimage.transform import resize

from train import ConvNet
from utils import read_image, cvt2Lab, upsample, cvt2rgb
import matplotlib.pyplot as plt

MODEL_PATH = "../model/image_colorization_model.pt"


def get_model():
    model = ConvNet()
    model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
    return model


def preprocess_image(inp_imgpath):
    img, real_size = read_image(inp_imgpath)
    img_light, _ = cvt2Lab(img)
    img_input = np.expand_dims(img_light, axis=0)
    img_input = np.expand_dims(img_input, axis=0)
    img_input = torch.autograd.Variable(torch.from_numpy(img_input).float(), requires_grad=False)
    print(str(img_light.shape) + 'preprocess')
    return img_light, img_input, real_size


def process_image(img, img_light):
    np.float = float
    print(str(img.shape) + 'before trans')

    img = np.squeeze(img, axis=0)
    img = np.transpose(img.astype(np.float), (1, 2, 0))
    print(str(img.shape) + 'after trans')

    img = upsample(img)
    print(str(img.shape) + 'after upscale')
    img = np.insert(img, 0, img_light, axis=2)
    img = (cvt2rgb(img) * 255.).astype(np.uint8)
    return img


def main(argv):
    if len(argv) != 2:
        print("Usage: python3 color_img.py input-image-path output-image-path")

    inp_imgpath, out_imgpath = argv[0], argv[1]
    model = get_model()

    img_light, img_input, real_size = preprocess_image(inp_imgpath)

    img = model(img_input).cpu().data.numpy()
    print(img.shape)
    img = process_image(img, img_light)

    img_result = Image.fromarray(img)
    img_result = img_result.resize((real_size[1], real_size[0]))
    img_result.save(out_imgpath, quality=90)
    print("Result image is saved to %s" % out_imgpath)
    return


if __name__ == '__main__':
    directory = 'C:\\Users\\andre\\PycharmProjects\\Coloring-greyscale-images\\Full-version\\Test'

    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            to_process = [f, os.path.join('C:\\Users\\andre\\PycharmProjects\\image-colorization\\out', filename)]
            main(to_process)
    # input = []
    # input.append('C:\\Users\\andre\\PycharmProjects\\image-colorization\\in\\369.jpg')
    # input.append('C:\\Users\\andre\\PycharmProjects\\image-colorization\\out\\testP.jpg')
    # main(input)
