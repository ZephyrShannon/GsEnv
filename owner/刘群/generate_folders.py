# <codecell>

import logging
import pgportfolio.autotrain.generate as generate
from pgportfolio.tools.configprocess import load_config
import os


def generate_folders(repeat):
    if not os.path.exists("./"  + "train_package"):
        os.makedirs("./" + "train_package")

    logging.basicConfig(level=logging.INFO)
    generate.add_packages(load_config(), repeat)


# <codecell>

