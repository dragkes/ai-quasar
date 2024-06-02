import torch
import numpy as np
from PIL import Image
from skimage import io, color
from skimage.transform import rescale, resize

MODEL_PATH = "../model/image_colorization_model-good.pt"


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
  return img_light, img_input, real_size


def process_image(img, img_light):
  img = np.squeeze(img, axis=0)
  img = np.transpose(img.astype(float), (1, 2, 0))
  img = upsample(img)
  print(str(img.shape) + 'after upscale')
  img = np.insert(img, 0, img_light, axis=2)
  img = (cvt2rgb(img) * 255.).astype(np.uint8)
  return img


class ConvNet(torch.nn.Module):
  """Convolutional network that performs image colorization."""

  def __init__(self, num_classes=10):
    super(ConvNet, self).__init__()
    self.layer1 = torch.nn.Sequential(
      torch.nn.Conv2d(1, 32, kernel_size=5, padding=2),
      torch.nn.ReLU(),
      torch.nn.BatchNorm2d(32),
      torch.nn.MaxPool2d(kernel_size=2)
    )

    self.layer2 = torch.nn.Sequential(
      torch.nn.Conv2d(32, 64, kernel_size=3, padding=1),
      torch.nn.ReLU(),
      torch.nn.BatchNorm2d(64),
      torch.nn.MaxPool2d(kernel_size=2)
    )

    self.layer3 = torch.nn.Sequential(
      torch.nn.Conv2d(64, 128, kernel_size=3, padding=1),
      torch.nn.ReLU(),
      torch.nn.BatchNorm2d(128),
      torch.nn.Conv2d(128, 64, kernel_size=3, padding=1),
      torch.nn.ReLU(),
      torch.nn.BatchNorm2d(64)
    )

    self.layer4 = torch.nn.Sequential(
      torch.nn.Conv2d(64, 32, kernel_size=3, padding=1),
      torch.nn.ReLU(),
      torch.nn.BatchNorm2d(32),
      torch.nn.Conv2d(32, 2, kernel_size=3, padding=1)
    )

    self.upsample = torch.nn.Upsample(scale_factor=4, mode='bilinear', align_corners=True)

    self.refine = torch.nn.Sequential(
      torch.nn.Conv2d(2, 32, kernel_size=3, padding=1),
      torch.nn.ReLU(),
      torch.nn.BatchNorm2d(32),
      torch.nn.Conv2d(32, 2, kernel_size=3, padding=1)
    )

  def forward(self, x):
    x = self.layer1(x)
    x = self.layer2(x)
    x = self.layer3(x)
    x = self.layer4(x)
    x = self.upsample(x)
    x = self.refine(x)
    return x


def read_image(filename, size=(256, 256), training=False):
  img = io.imread(filename)
  real_size = img.shape
  if img.shape != size and not training:
    img = resize(img, size, anti_aliasing=False)
  if len(img.shape) == 2:
    img = np.stack([img, img, img], 2)
  return img, real_size[:2]


def cvt2Lab(image):
  Lab = color.rgb2lab(image)
  return Lab[:, :, 0], Lab[:, :, 1:]  # L, ab


def cvt2rgb(image):
  return color.lab2rgb(image)


def upsample(image):
  scale = (1, 1, 1)
  return rescale(image, scale, mode='constant', order=3)
