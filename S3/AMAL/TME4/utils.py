import torch
import torch.nn as nn
from torch.utils.data import Dataset

device = "cpu"
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class RNN(nn.Module):
	def __init__(self,
		input_dim: int,
		latent_dim: int,
		output_dim: int,
		activ_latent=torch.tanh,
		activ_output=torch.sigmoid,
	):
		super().__init__()
		self.wx = torch.nn.Parameter(torch.randn(input_dim, latent_dim, device=device))
		self.wh = torch.nn.Parameter(torch.randn(latent_dim, device=device))
		self.bh = torch.nn.Parameter(torch.randn(latent_dim, device=device))
		self.wd = torch.nn.Parameter(torch.randn(latent_dim, output_dim, device=device))
		self.bd = torch.nn.Parameter(torch.randn(output_dim, device=device))
		self.activ_latent = activ_latent
		self.activ_output = activ_output
		self.input_dim = input_dim
		self.latent_dim = latent_dim
		self.output_dim = output_dim

	def one_step(self,
		x: torch.Tensor,	# batch * input_dim
		h: torch.Tensor		# batch * latent_dim
	):
		# output: batch * latent_dim
		return torch.mm(x, self.wx) + h*self.wh + self.bh

	def forward(self,
		X: torch.Tensor,		# length * batch * input_dim
		h: torch.Tensor	= None	# batch * latent_dim
	):
		# output: length * batch * latent_dim
		if h is None:
			h = torch.zeros(X.shape[1], self.latent_dim, device=device)
		length, batch, _ = X.shape
		output = torch.zeros(length, batch, h.shape[1], device=device)
		for i in range(length):
			h = self.one_step(X[i], h)
			output[i] = h
		return self.activ_latent(output)

	def decode(self,
		h: torch.Tensor
	):
		# output: batch * output_dim
		return self.activ_output(torch.mm(h, self.wd) + self.bd)


class SampleMetroDataset(Dataset):
	def __init__(self, data,length=20,stations_max=None):
		"""
			* data : tenseur des données au format  Nb_days x Nb_slots x Nb_Stations x {In,Out}
			* length : longueur des séquences d'exemple
			* stations_max : normalisation à appliquer
		"""
		self.data, self.length= data, length
		self.data = self.data.to(device)
		## Si pas de normalisation passée en entrée, calcul du max du flux entrant/sortant
		self.stations_max = stations_max if stations_max is not None else torch.max(self.data.view(-1,self.data.size(2),self.data.size(3)),0)[0]
		## Normalisation des données
		self.data = self.data / self.stations_max
		self.nb_days, self.nb_timeslots, self.classes = self.data.size(0), self.data.size(1), self.data.size(2)

	def __len__(self):
		## longueur en fonction de la longueur considérée des séquences
		return self.classes*self.nb_days*(self.nb_timeslots - self.length)

	def __getitem__(self,i):
		## transformation de l'index 1d vers une indexation 3d
		## renvoie une séquence de longueur length et l'id de la station.
		station = i // ((self.nb_timeslots-self.length) * self.nb_days)
		i = i % ((self.nb_timeslots-self.length) * self.nb_days)
		timeslot = i // self.nb_days
		day = i % self.nb_days
		return self.data[day,timeslot:(timeslot+self.length),station], station


class ForecastMetroDataset(Dataset):
	def __init__(self, data, length=20, stations_max=None):
		"""
			* data : tenseur des données au format  Nb_days x Nb_slots x Nb_Stations x {In,Out}
			* length : longueur des séquences d'exemple
			* stations_max : normalisation à appliquer
		"""
		self.data, self.length= data,length
		## Si pas de normalisation passée en entrée, calcul du max du flux entrant/sortant
		self.stations_max = stations_max if stations_max is not None else torch.max(self.data.view(-1,self.data.size(2),self.data.size(3)),0)[0]
		## Normalisation des données
		self.data = self.data / self.stations_max
		self.nb_days, self.nb_timeslots, self.classes = self.data.size(0), self.data.size(1), self.data.size(2)

	def __len__(self):
		## longueur en fonction de la longueur considérée des séquences
		return self.nb_days*(self.nb_timeslots - self.length)

	def __getitem__(self, i):
		## Transformation de l'indexation 1d vers indexation 2d
		## renvoie x[d,t:t+length-1,:,:], x[d,t+1:t+length,:,:]
		timeslot = i // self.nb_days
		day = i % self.nb_days
		return self.data[day,timeslot:(timeslot+self.length-1)],self.data[day,(timeslot+1):(timeslot+self.length)]

