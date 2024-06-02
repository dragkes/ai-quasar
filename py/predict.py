import numpy as np
from PIL import Image
import concurrent.futures

from keras.src.saving import load_model

# Путь к модели относительно текущего файла
model_path = 'model/photo_sharpen_model.h5'

# Параметр, определяющий насколько наложены одна на другую части изображения при их разделении на блоки
overlap = 10  # Можно менять, до 200 тояно, дальше не знаю, на 255 упало)


def split_image(image, size=(256, 256), overlap=0):
    width, height = image.size
    slices = []
    positions = []
    for x in range(0, width, size[0] - overlap):
        for y in range(0, height, size[1] - overlap):
            box = (x, y, min(x + size[0], width), min(y + size[1], height))
            slices.append(image.crop(box))
            positions.append((x, y))
    return slices, positions


def merge_images(slices, positions, original_size):
    width, height = original_size
    result = Image.new('RGB', (width, height))
    for slice_img, (x, y) in zip(slices, positions):
        result.paste(slice_img, (x, y))
    return result


def predict_slice(model, input_slice, target_size):
    input_slice_resized = input_slice.resize(target_size)
    input_slice_resized = np.array(input_slice_resized) / 255.0
    predicted_slice = model.predict(np.expand_dims(input_slice_resized, axis=0))[0]
    predicted_img = Image.fromarray((predicted_slice * 255).astype(np.uint8)).resize(input_slice.size)
    return predicted_img


def load_images(image):
    images = []
    original_sizes = []
    img = Image.fromarray(image)
    original_sizes.append(img.size)
    img = img.convert('RGB')  # Convert image to RGB
    images.append(np.array(img))
    return images, original_sizes


def sharpen(image):
    # Загрузка обученной модели
    model = load_model(model_path)

    # Загрузка изображений без изменения размера
    x_test, input_sizes = load_images(image)

    # Фиксированный размер для подачи в модель
    target_size = (256, 256)

    # Предсказание изображений по частям и их объединение
    predicted_images = []
    for input_img, original_size in zip(x_test, input_sizes):
      input_pil_img = Image.fromarray(input_img)
      input_slices, positions = split_image(input_pil_img, size=target_size, overlap=overlap)

      with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for input_slice in input_slices:
          futures.append(executor.submit(predict_slice, model, input_slice, target_size))
        predicted_slices = [future.result() for future in futures]

      predicted_img = merge_images(predicted_slices, positions, input_pil_img.size)
      predicted_images.append(predicted_img)

      return predicted_images[0]
