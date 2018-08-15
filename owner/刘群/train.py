# <codecell>

import pgportfolio.autotrain.training

def train (processes, device):
        train_dic, train_summary_df = pgportfolio.autotrain.training.train_all(processes, device)
        train_dic['train_summary'] = train_summary_df
        return train_dic


# <codecell>

