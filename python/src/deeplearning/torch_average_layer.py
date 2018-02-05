import torch

from torch.nn.modules import Module


class TorchAverageLayer(Module):
    def __init__(self):
        super(TorchAverageLayer, self).__init__()

    def forward(self, *input):
        emb = input[0]
        emb = torch.mean(emb, 1, True)
        return emb
