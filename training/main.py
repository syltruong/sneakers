from argparse import ArgumentParser

import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
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
        "--log_dir", type=str, required=True, help="output training logging dir"
    ) 
    parser.add_argument(
        "--learning_rate",
        type=float,
        required=True,
        default=1e-3,
        help="learning rate"
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
    parser.add_argument(
        "--num_workers", type=int, default=0, required=True, help="Number of dataloader workers"
    )
    parser.add_argument("--max_epochs", default=100, type=int, help="number of total epochs to run")

    args = parser.parse_args()

    dm = SneakerDataModule(image_folder=args.data_dir, batch_size=args.batch_size, num_workers=args.num_workers)
    dm.train_transforms = SimCLRTrainDataTransform(args.input_height)
    dm.val_transforms = SimCLREvalDataTransform(args.input_height)

    model = SimCLR(
        num_samples=dm.num_samples,
        batch_size=dm.batch_size,
        learning_rate=args.learning_rate,
        max_epochs=args.max_epochs,
        gpus=args.gpus,
        dataset="sneakers",
    )

    model_checkpoint_callback = ModelCheckpoint(
        monitor="val_loss",
        save_last=True,
        save_top_k=-1,
        period=10,
        filename='{epoch}-{val_loss:.2f}-{step}'
    )

    # TODO set the logger folder
    # Warning message is "Missing logger folder: /lightning_logs"
    trainer = pl.Trainer(
        default_root_dir=args.log_dir,
        callbacks = [model_checkpoint_callback],
        # checkpoint_callback=True,  # configures a default checkpointing callback
        max_epochs=args.max_epochs,
        gpus=args.gpus,
        accelerator='ddp' if args.gpus > 1 else None,
        enable_pl_optimizer=True if args.gpus > 1 else False,
    )

    trainer.fit(model, dm)


if __name__ == "__main__":
    main()