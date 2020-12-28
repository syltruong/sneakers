from pathlib import Path
from typing import List, Optional

import pytorch_lightning as pl
import torch
from PIL import Image
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms


class SneakerDataModule(pl.LightningDataModule):
    def __init__(
        self, image_folder: Path, batch_size: int, num_workers: int = 0, split: float = 0.8, seed: int = 1337
    ):
        """
        DataModule for sneakers dataset

        Parameters
        ----------
        image_folder : Path
            Path to the root image folder
            The dir structure needs to be as follows
                image_folder/
                    some_directory/
                        image1.png
                        image2.png
                        etc.
        batch_size : int
            Batch size
        split : float, optional
            Fraction of training samples, by default 0.8
        seed : int, optional
            splitting seed, by default 1337
        """

        super().__init__()
        self.image_folder = image_folder
        self.batch_size = batch_size
        self.num_workers = num_workers

        len_dataset = len(datasets.ImageFolder(image_folder))
        self.len_train = int(split * len_dataset)
        self.len_val = len_dataset - self.len_train
        self.num_samples = self.len_train

        self.seed = seed

    def default_transforms(self):
        return transforms.ToTensor()

    def train_dataloader(self):
        transforms = (
            self.default_transforms()
            if self.train_transforms is None
            else self.train_transforms
        )

        dataset = datasets.ImageFolder(self.image_folder, transform=transforms)

        dataset_train, _ = random_split(
            dataset,
            lengths=[self.len_train, self.len_val],
            generator=torch.Generator().manual_seed(self.seed),
        )

        return DataLoader(dataset=dataset_train, batch_size=self.batch_size, num_workers=self.num_workers)

    def val_dataloader(self):
        transforms = (
            self.default_transforms()
            if self.val_transforms is None
            else self.val_transforms
        )

        dataset = datasets.ImageFolder(self.image_folder, transform=transforms)

        _, dataset_val = random_split(
            dataset,
            lengths=[self.len_train, self.len_val],
            generator=torch.Generator().manual_seed(self.seed),
        )

        return DataLoader(dataset=dataset_val, batch_size=self.batch_size, num_workers=self.num_workers)
