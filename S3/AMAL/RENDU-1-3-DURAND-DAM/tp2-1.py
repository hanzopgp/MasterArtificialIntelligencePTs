from typing import List, Tuple
import torch
# from torch.utils.tensorboard import SummaryWriter
import datamaestro	# pip install datamaestro datamaestro-ml
import numpy as np


def init_params(
	*shape: torch.Size
) -> torch.Tensor:
	""" Init parameters """
	return torch.nn.Parameter(torch.randn(*shape))

def batch_gd(
	X: torch.Tensor,	# input, can be batch, mini-batch, or one sample
	Y: torch.Tensor,	# output tensor
	w: torch.Tensor,	# weights
	b: torch.Tensor,	# biases
	lr: float,			# learning rate
	epoch: int,			# number of training epochs
) -> List[float]:
	""" Implementation of BGD. Return list of loss after each epoch """

	loss_list = []
	for _ in range(epoch):
		Yhat = torch.mm(X, w) + b
		Yhat.retain_grad()
		
		loss = torch.sum((Yhat - Y) ** 2) / Y.shape[0]
		loss.backward()
		loss_list.append(float(loss))

		with torch.no_grad():
			w -= lr * w.grad
			b -= lr * b.grad
		w.grad.zero_()
		b.grad.zero_()

	return loss_list

def mini_batch_gd(
	X: torch.Tensor,	# input, can be batch, mini-batch, or one sample
	Y: torch.Tensor,	# output tensor
	w: torch.Tensor,	# weights
	b: torch.Tensor,	# biases
	lr: float,			# learning rate
	epoch: int,			# number of training epochs
	n_batch:int,		# number of batches
) -> List[float]:
	""" Implementation of MBGD. Return list of loss after each epoch """

	batch_size = X.shape[0] // n_batch
	loss_list = []
	for _ in range(epoch):
		idx = torch.randperm(X.shape[0])
		loss = 0.0
		for n in range(n_batch):
			batch_idx = idx[batch_size*n : batch_size*(n+1)]
			loss += batch_gd(
				X=X[batch_idx],
				Y=Y[batch_idx],
				w=w, b=b,
				lr=lr,
				epoch=1
			)[0]
		loss_list.append(loss / n_batch)

	return loss_list

def stoch_gd(
	X: torch.Tensor,	# input, can be batch, mini-batch, or one sample
	Y: torch.Tensor,	# output tensor
	w: torch.Tensor,	# weights
	b: torch.Tensor,	# biases
	lr: float,			# learning rate
	epoch: int,			# number of training epochs
) -> List[float]:
	""" Implementation of SGD. Return list of loss after each epoch """
	return mini_batch_gd(
		X=X, Y=Y,
		w=w, b=b,
		lr=lr,
		epoch=epoch,
		n_batch=X.shape[0]
	)

def make_boston_data() -> Tuple[torch.Tensor, torch.Tensor]:
	""" Download and normalize Boston housing data. Return x and y for training """
	data = datamaestro.prepare_dataset("edu.uci.boston")
	_, datax, datay = data.data()
	datax = torch.tensor(datax / np.linalg.norm(datax), dtype=torch.float)
	datay = torch.tensor(datay / np.linalg.norm(datay), dtype=torch.float).reshape(-1,1)
	return datax, datay


if __name__ == "__main__":
	# writer = SummaryWriter()
	datax, datay = make_boston_data()
	w = init_params(datax.shape[1], datay.shape[1])
	b = init_params(datay.shape[1])

	# l = batch_gd(X=datax, Y=datay, w=w, b=b, lr=0.05, epoch=50)
	l = mini_batch_gd(X=datax, Y=datay, w=w, b=b, lr = 0.01, epoch = 50, n_batch=10)
	# l = stoch_gd(X=datax, Y=datay, w=w, b=b, lr = 0.001, epoch=10)

	[print(loss) for loss in l]