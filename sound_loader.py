import torch
import numpy as np
from pathlib import Path
import utils.irutilities as irutil

np.random.seed(0)
torch.manual_seed(0)

class sound_samples(torch.utils.data.Dataset):
    def __init__(self):
        # Load dataset
        path = Path('mesh_rir/S32-M441_npy/')
        self.spectrograms = np.load(path.joinpath('spectrograms.npy'), mmap_mode='r+')
        
        self.posMic, self.posSrc, _ = irutil.loadIR(path)

        # Calculate min_xy
        min_x = min(np.min(self.posMic[0]), np.min(self.posSrc[0]))
        min_y = min(np.min(self.posMic[1]), np.min(self.posSrc[1]))
        self.min_xy = (min_x, min_y)

        # Calculate max_xy
        max_x = max(np.max(self.posMic[0]), np.max(self.posSrc[0]))
        max_y = max(np.max(self.posMic[1]), np.max(self.posSrc[1]))
        self.max_xy = (max_x, max_y)

        # Join in a single list of (src, mic, IR) objects
        self.indices = []

        for s in range(len(self.posSrc)):
            for m in range(len(self.posMic)):
                self.indices.append([s,m])
                
    def __len__(self):
        return  len(self.indices)

    def __getitem__(self, idx):
        s, m = self.indices[idx]
        src = self.posSrc[s]
        mic = self.posMic[m]
        spectrogram = self.spectrograms[s,m]
        return src, mic, spectrogram
