
import torch
import torch.nn as nn
from torch.nn import CrossEntropyLoss
from torch.utils.data import DataLoader
from torch.nn.functional import one_hot
from torch.utils.tensorboard import SummaryWriter
from textloader import *
from generate import *

device = "cpu"

def maskedCrossEntropy(output: torch.Tensor, target: torch.LongTensor, padcar: int):
	"""
	:param output: Tenseur length x batch x output_dim,
	:param target: Tenseur length x batch
	:param padcar: index du caractere de padding
	"""
	mask = torch.where(output.argmax(axis=1)==padcar, 0, 1)
	loss = CrossEntropyLoss(reduction="none")
	loss_tensor = mask * loss(output, target)
	return loss_tensor.mean() 

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


class LSTM(RNN):
    pass


class GRU(nn.Module):
    pass



#  TODO:  Reprenez la boucle d'apprentissage, en utilisant des embeddings plutôt que du one-hot

# output = torch.tensor([[0.2,0.2,0.6],[0.2,0.2,0.6],[0.2,0.6,0.2],[0.6,0.2,0.2],[0.6,0.2,0.2],[0.6,0.2,0.2]])
# output = torch.tensor([[0,0,1],[0,0,1],[0,1,0],[1,0,0],[1,0,0],[1,0,0]]).float()
# target = torch.tensor([2,2,1,0,0,0], dtype=torch.int64)
# padcar = 0
# print(maskedCrossEntropy(output, target, padcar))

PATH = "../data/"
with open(PATH+"trump_full_speech.txt","r") as f:
    txt = f.read()
# loaded_tensor = torch.tensor(loaded_list)
ds = TextDataset(txt)
loader = DataLoader(ds, collate_fn=pad_collate_fn, batch_size=3)
data = next(iter(loader))

print(data.shape)

print(generate(RNN(ds.maxlen, 64, 97), string2code, code2string, EOS_IX, start="", maxlen=200))
