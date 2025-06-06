import argparse
import os
import random
import json

import numpy as np
import torch
import torch.backends.cudnn as cudnn

import lavis.tasks as tasks
from lavis.common.config import Config
from lavis.common.dist_utils import get_rank, init_distributed_mode
from lavis.common.logger import setup_logger
from lavis.common.registry import registry
from lavis.datasets.builders import *
from lavis.models import *
from lavis.processors import *
from lavis.runners import *
from lavis.tasks import *

def parse_args():
    parser = argparse.ArgumentParser(description="Testing")
    parser.add_argument("--cfg-path", required=True, help="path to configuration file.")
    parser.add_argument("--output-file", default="predictions.json", help="File to save predictions.")
    parser.add_argument("--options", nargs="+", help="Override some settings in the config.")
    return parser.parse_args()

def setup_seeds(config):
    seed = config.run_cfg.seed + get_rank()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    cudnn.benchmark = False
    cudnn.deterministic = True

def get_runner_class(cfg):
    return registry.get_runner_class(cfg.run_cfg.get("runner", "runner_base"))

def main():
    args = parse_args()
    cfg = Config(args)

    # Override evaluation mode
    cfg.run_cfg.evaluate = True
    cfg.run_cfg.train_splits = []
    cfg.run_cfg.valid_splits = []
    cfg.run_cfg.test_splits = ["test"]  # Change to test split name if available

    init_distributed_mode(cfg.run_cfg)
    setup_seeds(cfg)
    setup_logger()

    cfg.pretty_print()

    task = tasks.setup_task(cfg)
    datasets = task.build_datasets(cfg)
    model = task.build_model(cfg)

    runner = get_runner_class(cfg)(
        cfg=cfg, job_id="test_run", task=task, model=model, datasets=datasets
    )

    runner.evaluate()

    # Save predictions
    if get_rank() == 0:
        with open(args.output_file, "w") as f:
            json.dump(predictions, f, indent=2)
        print(f"Predictions saved to {args.output_file}")

if __name__ == "__main__":
    main()

