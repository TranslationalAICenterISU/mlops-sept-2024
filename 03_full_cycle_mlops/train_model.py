import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import os
import mlflow
import wandb

class AutoEncoder(nn.Module):
    def __init__(self):
        super(AutoEncoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 16, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, 7)
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(64, 32, 7),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 16, 3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(16, 1, 3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

class HouseDataset(Dataset):
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((128, 128)),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = os.path.join(self.folder_path, self.image_files[idx])
        image = Image.open(img_path)
        image = self.transform(image)
        return image

def train_model():
    mlflow.set_experiment("House Autoencoder")
    wandb.init(project="house-autoencoder", config={"epochs": 2, "batch_size": 32})

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoEncoder().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters())

    dataset = HouseDataset("processed_images")
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    with mlflow.start_run() as run:
        for epoch in range(2):
            for batch in dataloader:
                inputs = batch.to(device)
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, inputs)
                loss.backward()
                optimizer.step()

                mlflow.log_metric("loss", loss.item())
                wandb.log({"loss": loss.item()})

            # Log sample images
            with torch.no_grad():
                sample_inputs = next(iter(dataloader)).to(device)
                sample_outputs = model(sample_inputs)
                wandb.log({"input_images": [wandb.Image(img) for img in sample_inputs[:4]]})
                wandb.log({"output_images": [wandb.Image(img) for img in sample_outputs[:4]]})

        mlflow.pytorch.log_model(model, "model")
        wandb.save("model.pth")
        # Save the run ID to a file
        with open("mlflow_run_id.txt", "w") as f:
            f.write(run.info.run_id)

if __name__ == "__main__":
    train_model()