from pathlib import Path
from re import X
import torch
from torchvision.utils import make_grid
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F
# from torch.utils.tensorboard import SummaryWriter
import numpy as np
from datamaestro import prepare_dataset
from tqdm import tqdm
import datetime
from torch.utils.tensorboard import SummaryWriter
from matplotlib import pyplot as plt

# Tensorboard : rappel, lancer dans une console tensorboard --logdir runs
writer = SummaryWriter("runs/runs"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

# Pour visualiser
# Les images doivent etre en format Channel (3) x Hauteur x Largeur
# images = torch.tensor(train_images[0:8]).unsqueeze(1).repeat(1,3,1,1).double()/255.
# Permet de fabriquer une grille d'images
# images = make_grid(images)
# Affichage avec tensorboard
# writer.add_image(f'samples', images, 0)

ITERATIONS = 100
BATCH_SIZE = 16
LEARNING_RATE = 1e-3

savepath = Path("model.pch")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("cpu")


class MyDataset(Dataset):
	def __init__(self, datax:np.ndarray, datay:np.ndarray):
		self.datax = torch.tensor(datax / 255, dtype=torch.float32)
		self.datay = torch.tensor(datay)

	def __getitem__(self, idx):
		return self.datax[idx].reshape(-1), self.datay[idx]

	def __len__(self):
		return len(self.datay)


class State:
	def __init__(self, model:nn.Module, optim:torch.optim.Optimizer, loss:nn.Module):
		self.model = model
		self.optim = optim
		self.loss = loss
		self.epoch = self.iteration = 0


class AutoEncoder(nn.Module):
	def __init__(self, input_dim:int, compress_dim:int):
		super().__init__()
		self.model = nn.Sequential(
			nn.Linear(input_dim, compress_dim),
			nn.ReLU(),
			nn.Linear(compress_dim, input_dim),
			nn.Sigmoid()
		).to(device)
		self.optim = torch.optim.Adam(self.model.parameters(), lr=LEARNING_RATE)
		self.loss = nn.MSELoss()

class HighwayModel(nn.Module):
	def __init__(self, n_neurons, n_layers, activation_function):
		super(HighwayModel, self).__init__()
		# super().__init__()
		self.n_layers = n_layers
		self.model = [nn.Linear(n_neurons, n_neurons) for _ in range(n_layers*3)]
		self.activation_function = activation_function

	def forward(self, x):
		for n, layer in enumerate(range(self.n_layers)):
			gate = F.sigmoid(self.model[n](x))
			nonlinear = self.activation_function(self.model[n](x))
			linear = self.model[n](x)
			x = gate * nonlinear + (1 - gate) * linear
		return x

if __name__ == '__main__':
	data = prepare_dataset("com.lecun.mnist");
	train_images, train_labels = data.train.images.data(), data.train.labels.data()
	test_images, test_labels =  data.test.images.data(), data.test.labels.data()

	data = MyDataset(train_images, train_labels)
	train_data = DataLoader(data, shuffle=True, batch_size=BATCH_SIZE)
	num_batch = 0
	for x, y in train_data:
		num_batch += 1
	print("Batch size:", BATCH_SIZE)
	print("Number of batches:", num_batch)

	# model_chosen = AutoEncoder(data[0][0].shape[0], 64)
	model_chosen = HighwayModel(784, 3, torch.nn.functional.relu)

	if savepath.is_file():
		with savepath.open('rb') as f:
			state = torch.load(f)
	else:
		state = State(model_chosen.model, model_chosen.optim, model_chosen.loss)

	for ep in tqdm(range(state.epoch)):
		for x, _ in train_data:
			state.optim.zero_grad()
			x = x.to(device)
			xhat = state.model(x)
			state.loss(xhat, x).backward()
			state.optim.step()
			state.iteration += 1
			writer.add_scalar("Train loss", ((x - xhat)**2).mean(), ep)
		with savepath.open('wb') as f:
			state.epoch = ep + 1
			torch.save(state, f)

	# Highway model
	# model = HighwayModel(784, 3, torch.nn.functional.relu)
	# for x, _ in train_data:
	# 	print(x)
	# 	out = model(x)
	# 	print(out)
	# 	break
	# plt.imshow(x[0].reshape(28,28).detach().numpy())
	# plt.imshow(out[0].reshape(28,28).detach().numpy())






			
