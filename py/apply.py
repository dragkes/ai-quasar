import torch
from PIL import Image
from torch import nn
from torchvision import transforms
import matplotlib.pyplot as plt


MODEL_PATH = "model/unet_glare_removal.pth"


class UNet(nn.Module):
    def __init__(self, in_channels=3, out_channels=3):
        super(UNet, self).__init__()

        def CBR(in_channels, out_channels):
            return nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(inplace=True)
            )

        self.enc1 = CBR(in_channels, 64)
        self.enc2 = CBR(64, 128)
        self.enc3 = CBR(128, 256)
        self.enc4 = CBR(256, 512)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.upconv4 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        self.dec4 = CBR(512, 256)
        self.upconv3 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.dec3 = CBR(256, 128)
        self.upconv2 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.dec2 = CBR(128, 64)
        self.dec1 = nn.Conv2d(64, out_channels, kernel_size=1)

    def forward(self, x):
        enc1 = self.enc1(x)
        enc2 = self.enc2(self.pool(enc1))
        enc3 = self.enc3(self.pool(enc2))
        enc4 = self.enc4(self.pool(enc3))

        dec4 = self.upconv4(enc4)
        dec4 = torch.cat((dec4, enc3), dim=1)
        dec4 = self.dec4(dec4)
        dec3 = self.upconv3(dec4)
        dec3 = torch.cat((dec3, enc2), dim=1)
        dec3 = self.dec3(dec3)
        dec2 = self.upconv2(dec3)
        dec2 = torch.cat((dec2, enc1), dim=1)
        dec2 = self.dec2(dec2)
        dec1 = self.dec1(dec2)

        return torch.sigmoid(dec1)


# Load the trained model
model = UNet().cpu()
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

# Transformations
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])


def remove_glare(image):
    # Load and transform the image
    image = Image.fromarray(image)
    image = image.convert('RGB')
    input_tensor = transform(image).unsqueeze(0).cpu()  # Add batch dimension

    # Inference
    with torch.no_grad():
        output_tensor = model(input_tensor)

    # Convert tensor to image
    output_image = transforms.ToPILImage()(output_tensor.squeeze(0))

    # Save the output image
    return output_image


def main():
    # Remove glare from an example image
    image_path = 'C:\\Users\\andre\\PycharmProjects\\Glare\\output\\22.jpg'
    img = Image.open(image_path)
    result = remove_glare(img)
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    axs[0].imshow(img)
    axs[0].set_title('Original Image')
    axs[1].imshow(result)
    axs[1].set_title('Processed Image')
    for ax in axs:
        ax.axis('off')
    plt.show()


if __name__ == '__main__':
    main()
