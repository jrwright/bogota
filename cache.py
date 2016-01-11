from gambit.nash import ExternalSolver

NASH_CACHE = {}

def find_key(game):
    return (str(game) in NASH_CACHE)

def put_eqa(game, eqa):
    NASH_CACHE[str(game)] = eqa

def get_eqa(game):
    return NASH_CACHE[str(game)]

def _load_eqa(game, filename):
    """
    If `filename` exists, then read in its equilibria and cache them as
    equilibria of `game`.
    """
    s = ExternalSolver()
    try:
        with open(filename, 'rt') as f:
            profiles = s._parse_output(f, game, False)
            put_eqa(game, profiles)
    except:
        try:
            with open(filename, 'rt') as f:
                profiles = s._parse_output(f, game, True)
                put_eqa(game, profiles)
        except:
            pass


