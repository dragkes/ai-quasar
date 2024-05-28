import os
import cv2


def resize_images(input_folder, output_folder, size=(64, 64)):
    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all files in the input folder
    for filename in os.listdir(input_folder):
        # Construct full file path
        file_path = os.path.join(input_folder, filename)

        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Read the image
            image = cv2.imread(file_path)

            # Resize the image
            resized_image = cv2.resize(image, size)

            # Construct the output file path
            output_file_path = os.path.join(output_folder, filename)

            # Write the resized image to the output folder
            cv2.imwrite(output_file_path, resized_image)

    print(f"All images have been resized and saved to {output_folder}")


def write_filenames_to_txt(input_folder, output_file):
    # Get a list of all files in the input folder
    filenames = os.listdir(input_folder)

    # Filter out directories, we only want files
    filenames = [f for f in filenames if os.path.isfile(os.path.join(input_folder, f))]

    # Open the output file in write mode
    with open(output_file, 'w') as file:
        # Write each filename to the text file
        for filename in filenames:
            file.write(filename + '\n')

    print(f"All file names have been written to {output_file}")
def main():
    # Example usage
    input_folder = 'C:\\Users\\andre\\PycharmProjects\\image-colorization\\dataset\\gray_image'
    output_folder = 'C:\\Users\\andre\\PycharmProjects\\image-colorization\\dataset\\gray_image_resized'
    resize_images(input_folder, output_folder)
    #write_filenames_to_txt(input_folder, 'output_filenames.txt')

if __name__ == '__main__':
    main()
