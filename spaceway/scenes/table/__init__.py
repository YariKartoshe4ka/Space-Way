from .objects import TableBackButton, TableScore


def init(screen, base_dir, config):
    score = TableScore(screen, base_dir, config)
    back = TableBackButton(screen, base_dir, config)

    return score, back
