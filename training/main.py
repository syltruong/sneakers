from argparse import ArgumentParser

import pytorch_lightning as pl
from pl_bolts.models.self_supervised import SimCLR
from pl_bolts.models.self_supervised.simclr.transforms import (
    SimCLREvalDataTransform,
    SimCLRTrainDataTransform,
)

from training.sneaker_data_module import SneakerDataModule


def main():

    parser = ArgumentParser()
    parser.add_argument(
        "--data_dir", type=str, required=True, help="path to the folder of images"
    )
    parser.add_argument(
        "--input_height",
        type=int,
        required=True,
        help="height of image input to SimCLR",
    )
    parser.add_argument("--batch_size", type=int, default=1024, required=True)
    parser.add_argument(
        "--gpus", type=int, default=0, required=True, help="Number of GPUs"
    )
    parser.add_argument("--max_epochs", default=100, type=int, help="number of total epochs to run")

    args = parser.parse_args()

    dm = SneakerDataModule(image_folder=args.data_dir, batch_size=args.batch_size)
    dm.train_transforms = SimCLRTrainDataTransform(args.input_height)
    dm.val_transforms = SimCLREvalDataTransform(args.input_height)

    model = SimCLR(
        num_samples=dm.num_samples,
        batch_size=dm.batch_size,
        max_epochs=args.max_epochs,
        gpus=args.gpus,
        dataset="sneakers",
    )

    trainer = pl.Trainer(
        checkpoint_callback=True,  # configures a default checkpointing callback
        max_epochs=args.max_epochs,
        gpus=args.gpus,
        accelerator='dp' if args.gpus > 1 else None,
    )

    trainer.fit(model, dm)
