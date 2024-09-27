# Import necessary libraries
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
import pytorch_lightning as pl
from pytorch_lightning import Trainer
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Define a simple neural network
class SimpleNN(pl.LightningModule):
    def __init__(self):
        super(SimpleNN, self).__init__()
        # A simple feed-forward network with two fully connected layers
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # Flatten the image to a vector
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)

    def training_step(self, batch, batch_idx):
        # Training step - forward pass and loss computation
        data, target = batch
        output = self(data)
        loss = F.nll_loss(output, target)
        return loss

    def configure_optimizers(self):
        # Define an optimizer for training
        return optim.Adam(self.parameters(), lr=1e-3)

# Data preparation using the MNIST dataset
def prepare_data():
    # MNIST dataset with basic normalization
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    train_dataset = datasets.MNIST(root='./mnist_data', train=True, transform=transform, download=True)
    return DataLoader(train_dataset, batch_size=64, shuffle=True)

# Instantiate the model
model = SimpleNN()

# Prepare the data
train_loader = prepare_data()

# Number of GPUs available
gpus = torch.cuda.device_count()

# Define the PyTorch Lightning trainer with multi-node and multi-GPU support
trainer = Trainer(
    max_epochs=5,         # Number of epochs
    devices=2,
    accelerator='gpu',
    # num_nodes=1,          # Number of nodes
    # strategy='ddp',       # Distributed Data Parallel strategy
    default_root_dir="./mnist_multi_node_demo"  # Directory to save checkpoints
)

# Fit the model
trainer.fit(model, train_loader)
