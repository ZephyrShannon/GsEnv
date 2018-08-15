# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools.gsUtils import ExtractDictModelData as Extract


def extract_input_to_panel(context,model,oset_idx):
    panel_input = Extract(model)
    return panel_input.get_input_factor(oset_idx)
