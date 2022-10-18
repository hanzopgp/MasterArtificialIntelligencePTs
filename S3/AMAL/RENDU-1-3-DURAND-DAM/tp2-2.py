from typing import List
import torch
import datamaestro
from typing import Tuple
import numpy as np
from torch.utils.tensorboard import SummaryWriter


def make_boston_data() -> Tuple[torch.Tensor, torch.Tensor]:
	""" Download and normalize Boston housing data. Return x and y for training """
	data = datamaestro.prepare_dataset("edu.uci.boston")
	_, datax, datay = data.data()
	datax = torch.tensor(datax / np.linalg.norm(datax), dtype=torch.float)
	datay = torch.tensor(datay / np.linalg.norm(datay), dtype=torch.float).reshape(-1,1)
	return datax, datay

def train_modular_net(
	X: torch.Tensor,
	Y: torch.Tensor,
	hidden_nodes: int,
	lr: float,
	epoch: int,
	writer: SummaryWriter
):
	""" Implement manual training of a modular network. Return list of loss after each epoch """
	network: List[torch.nn.Module] = [
		torch.nn.Linear(X.shape[1], hidden_nodes),
		torch.nn.Tanh(),
		torch.nn.Linear(hidden_nodes, Y.shape[1]),
		torch.nn.MSELoss()
	]
	params = []
	for m in network:
		params += list(m.parameters())
	optim = torch.optim.SGD(params, lr=lr)
	
	for i in range(epoch):
		optim.zero_grad()
		x = datax
		for m in network[:-1]:
			x = m.forward(x)	
		loss = network[-1].forward(x, datay)
		loss.backward()
		optim.step()
		writer.add_scalar('Loss/modular', float(loss), i)

def train_sequential_net(
	X: torch.Tensor,
	Y: torch.Tensor,
	hidden_nodes: int,
	lr: float,
	epoch: int,
	writer: SummaryWriter
):
	""" Implement auto training of a sequential network. Return list of loss after each epoch """
	network = torch.nn.Sequential(
		torch.nn.Linear(X.shape[1], hidden_nodes),
		torch.nn.Tanh(),
		torch.nn.Linear(hidden_nodes, Y.shape[1])
	)
	loss_module = torch.nn.MSELoss()
	optim = torch.optim.SGD(list(network.parameters()) + list(loss_module.parameters()), lr=lr)
	
	for i in range(epoch):
		optim.zero_grad()
		output = network.forward(datax)
		loss = loss_module.forward(output, datay)
		loss.backward()
		optim.step()
		writer.add_scalar('Loss/sequential', float(loss), i)


if __name__ == "__main__":
	writer = SummaryWriter()

	datax, datay = make_boston_data()

	modular_l = train_modular_net(
		X=datax, Y=datay,
		hidden_nodes=128,
		lr=0.01, epoch=1000,
		writer=writer
	)

	sequential_l = train_sequential_net(
		X=datax, Y=datay,
		hidden_nodes=128,
		lr=0.01, epoch=1000,
		writer=writer
	)