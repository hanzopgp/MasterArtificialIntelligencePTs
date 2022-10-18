from utils import RNN, device, ForecastMetroDataset

from torch.utils.data import  DataLoader
import torch

# Nombre de stations utilisé
CLASSES = 10
# Longueur des séquences
LENGTH = 20
# Dimension de l'entrée (1 (in) ou 2 (in/out))
DIM_INPUT = 2
# Taille du batch
BATCH_SIZE = 32
# Taille de la seq predite
HORIZON = 5

PATH = "data/"


# Taille X: LENGTH
# Taille h: LENGTH + HORIZON
# Taille Y: HORIZON
# On predict 


matrix_train, matrix_test = torch.load(open(PATH+"hzdataset.pch", "rb"))
ds_train = ForecastMetroDataset(
    matrix_train[:, :, :CLASSES, :DIM_INPUT], length=LENGTH)
ds_test = ForecastMetroDataset(
    matrix_test[:, :, :CLASSES, :DIM_INPUT], length=LENGTH, stations_max=ds_train.stations_max)
data_train = DataLoader(ds_train, batch_size=BATCH_SIZE, shuffle=True)
data_test = DataLoader(ds_test, batch_size=BATCH_SIZE, shuffle=False)
del matrix_train, matrix_test

EPOCH = 100
DIM_LATENT = 16

model = RNN(DIM_INPUT, DIM_LATENT, CLASSES, activ_output=torch.nn.Softmax(dim=1))
optim = torch.optim.Adam(model.parameters())
loss = torch.nn.CrossEntropyLoss()


for i in range(EPOCH):
	# Training
	for X, Y in data_train:
		h = None
		X = torch.movedim(X, 0, 1)
		Y = Y.to(device)
		optim.zero_grad()
		Yhat = model(X, h)
		h = Yhat[-1]
		loss(model.decode(h), Y).backward()
		optim.step()
	
	# Testing
	with torch.no_grad():
		total = correct = 0
		for X, Y in data_test:
			h = None
			X = torch.movedim(X, 0, 1)
			Y = Y.to(device)
			Yhat = model(X, h)
			h = Yhat[-1]
			prediction = model.decode(h).argmax(dim=1)
			correct += torch.sum(prediction == Y)
			total += len(Y)
	print(f"Epoch {i} accuracy {correct / total}")