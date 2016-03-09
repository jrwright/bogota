from gambit.nash import ExternalSolver

# ============================== Nash equilibria ==============================

# game -> [equilibrium]
NASH_CACHE = {}

def find_eqm_key(game):
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
        # Try again by reading rationals instead of floats
        try:
            with open(filename, 'rt') as f:
                profiles = s._parse_output(f, game, True)
                put_eqa(game, profiles)
        except:
            pass

# ==================================== QREs ===================================

# game -> {lam -> QRE}
QRE_CACHE = {}

def find_qre_key(game, lam, tol):
    """
    Return True if `game` has cached QREs.
    """
    if (str(game) not in QRE_CACHE):
        return False
    h = QRE_CACHE[str(game)]
    if lam in h:
        return True
    if tol <= 0.0:
        return False

    newlam = min(h.keys(), key=lambda l:abs(lam - l))
    if abs(newlam - lam) <= tol:
        return True
    else:
        return False


def put_qres(game, qs):
    if str(game) not in QRE_CACHE:
        QRE_CACHE[str(game)] = qs
    else:
        QRE_CACHE[str(game)].update(qs)

def get_qre(game, lam, tol=0.0005):
    """
    Return the cached QRE of `game` with precision `lam`.  If `nearest` is True
    and there is no cached QRE with precision exactly `lam`, then return the
    nearest match that is within `tol`.
    Returns only exact matches if `tol` is 0.0.
    """
    h = QRE_CACHE[str(game)]
    try:
        return h[lam]
    except KeyError:
        if tol <= 0.0:
            raise
        newlam = min(h.keys(), key=lambda l:abs(lam - l))
        if abs(newlam - lam) <= tol:
            return h[newlam]
        else:
            raise

def _load_qres(game, filename):
    """
    If `filename` exists, then read in its QREs and cache them as QREs of
    `game`.
    """
    try:
        with open(filename, 'rt') as f:
            qs = {}
            for line in f:
                entries = line.strip().split(",")
                profile = game.mixed_strategy_profile()
                lam = float(entries[0])
                for (i, p) in enumerate(entries[1:]):
                    profile[i] = float(p)
                qs[lam] = profile
            put_qres(game, qs)
    except:
        pass
