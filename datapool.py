"""
Implement classes for representing data pools.
"""

# TODO - This system works fine for fully-observable strategies, but when we
# get to Bayesian games it is not going to work so well anymore, because we
# will know what "ex_ante actions" were taken by each "ex_ante player", but we
# won't know which type was which.

import math
from numpy import inf, array
from numpy.random import RandomState
import gambit
from bogota.utils import normalize, make_profile, action_profiles


class DataPool(object):
    """
    A DataPool is an iterable collection of WeightedProfile objects, representing empirical
    distributions of play.
    """
    def __init__(self, weighted_profiles, name=None):
        self._name=name
        self._weighted_profiles = list(weighted_profiles)

    def rv(self, name, game_model, model_args, **stochastic_args):
        """
        Return a random variable named 'name' representing this data using
        'game_model' parameterized by 'model_args'.
        """
        assert 'keys' in dir(model_args), "model_args must be a dict-like object"
        import pymc as pm
        def datapool_logp(value, **args):
            return sum([ wp.log_likelihood(game_model(wp.game, **args)) \
                         for wp in value._weighted_profiles ])

        try:
            model_name = game_model.__name__
        except AttributeError:
            model_name = str(game_model)

        return pm.Stochastic(name = name,
                             doc = "<DataPool.rv '%s'>" % model_name,
                             logp = datapool_logp,
                             parents = model_args,
                             value = self,
                             dtype = DataPool,
                             observed = True,
                             trace = False,
                             **stochastic_args)

    def log_likelihood(self, predictor):
        """
        Given a callable 'predictor' that maps from a game to a predicted profile of play, return
        the log likelihood of the data pool's data given the predictions of 'predictor'.
        """
        return sum([ wp.log_likelihood(predictor(wp.game)) for wp in self._weighted_profiles ])

    def uniform_log_likelihood(self):
        """
        Return the log likelihood of this dataset according to a prediction that
        agents uniformly randomize over their actions.  (For normalization)
        """
        return self.log_likelihood(lambda g: g.mixed_profile())

    def __iter__(self):
        return self._weighted_profiles.__iter__()

    @property
    def n(self):
        """
        The number of independent observations in the pool.  This is not the same as the number of
        WeightedProfiles in the pool, since each WeightedProfile will typically contain represent
        multiple independent observations.
        """
        return sum([ wp.n for wp in self._weighted_profiles ])

    @property
    def weighted_profiles(self):
        """
        A list of WeightedProfile objects containing the observations of this pool.
        """
        return self._weighted_profiles[:]

    @property
    def games(self):
        """
        The games for which this pool contains observations.
        """
        return [ w.game for w in self._weighted_profiles ]

    def test_and_train(self, seed, test_fraction):
        """
        Randomly select ``test_fraction`` of the datapoints in the pool and return
        two new pools containing the selected and unselected data respectively.
        """
        r = RandomState(seed)
        test_sz = int(round(self.n * test_fraction))
        test_dnps = self._blank_denormalized()
        train_dnps = [wp.denormalized_profile() for wp in self._weighted_profiles]
        self._select_points(r, test_dnps, train_dnps, test_sz)

        return [self._denormalized_list_to_pool(test_dnps),
                self._denormalized_list_to_pool(train_dnps)]

    def test_validation_train(self, seed, test_fraction, validation_fraction):
        """
        Randomly select ``test_fraction`` and ``validation_fraction`` of the
        datapoints in the pool and return three new pools containing the
        selected and unselected data respectively.
        """
        r = RandomState(seed)
        test_sz = int(round(self.n * test_fraction))
        validation_sz = int(round(self.n * validation_fraction))
        test_dnps = self._blank_denormalized()
        validation_dnps = self._blank_denormalized()
        train_dnps = [wp.denormalized_profile() for wp in self._weighted_profiles]
        self._select_points(r, test_dnps, train_dnps, test_sz)
        self._select_points(r, validation_dnps, train_dnps, validation_sz)

        return [self._denormalized_list_to_pool(test_dnps),
                self._denormalized_list_to_pool(validation_dnps),
                self._denormalized_list_to_pool(train_dnps)]

    def test_validation_train_game_wise(self, seed=None, test_fraction=0.1,
                                        validation_fraction=0.1):
        """
        Randomly select ``test_fraction`` and ``validation_fraction`` of the unique
        games (as defined by their payoff structure) in the pool and then return 
        three new pools containing the datapoints from the selected and unselected 
        games respectively.
        """
        r = RandomState(seed)
        train_fraction = 1 - test_fraction - validation_fraction
        games = self._generate_game_dictionary()
        game_idx = games.keys()

        n = len(game_idx)
        test_sz = int(round(n*test_fraction))
        valid_sz = int(round(n*validation_fraction))
        train_sz = n - test_sz - valid_sz

        indices = array(range(n))
        r.shuffle(indices)

        train = []
        for idx in indices[0:train_sz]:
            train = train + [wp for wp in games[game_idx[idx]]]

        valid = []
        for idx in indices[train_sz:(train_sz+valid_sz)]:
            valid = valid + [wp for wp in games[game_idx[idx]]]

        test = []
        for idx in indices[(train_sz + valid_sz):n]:
            test = test + [wp for wp in games[game_idx[idx]]]
        return [DataPool(test), DataPool(valid), DataPool(train)]

    def test_fold(self, seed, num_folds, fold_idx):
        """
        Return a `DataPool` of the ``fold_idx``th fold out of ``num_folds`` folds
        divided using random ``seed``.
        """
        folds = self._divide_folds(seed, num_folds)
        return self._denormalized_list_to_pool(folds[fold_idx])

    def train_fold(self, seed, num_folds, fold_idx, return_both=False):
        train_dnps = [wp.denormalized_profile() for wp in self._weighted_profiles]
        test_dnps = [wp.denormalized_profile() for wp in self.test_fold(seed, num_folds, fold_idx)]
        # Easiest is to just decrement the grand pool by the testing points
        for j in xrange(len(test_dnps)):
            for (i,n) in enumerate(test_dnps[j]):
                train_dnps[j][i] -= test_dnps[j][i]
        if return_both:
            return (self._denormalized_list_to_pool(train_dnps),
                    self._denormalized_list_to_pool(test_dnps))
        else:
            return self._denormalized_list_to_pool(train_dnps)

    # TODO make gamewise an argument to train_fold and remove this fn?
    def train_fold_gamewise(self, seed, num_folds, fold_idx,
                            return_both=False, stratified=False):
        folds = self._divide_folds_gamewise(num_folds, seed, stratified)
        test = self._denormalized_list_to_pool([wp.denormalized_profile()
                                               for wp in folds[fold_idx]])
        train = []
        for i, fold in enumerate(folds):
            if i != fold_idx:
                train += [wp.denormalized_profile() for wp in fold]
        train = self._denormalized_list_to_pool(train)
        if return_both:
            return train, test
        else:
            return train

    def test_fold_gamewise(self, seed, num_folds, fold_idx, stratified=False):
        folds = self._divide_folds_gamewise(num_folds, seed, stratified)
        return self._denormalized_list_to_pool([wp.denormalized_profile()
                                               for wp in folds[fold_idx]])

    # Keeping this function for BGTNet project.
    def test_validation_train_folds_gamewise(self, seed, num_folds, fold_idx, stratified=False):
        folds = self._divide_folds_gamewise(num_folds, seed, stratified)
        test = self._denormalized_list_to_pool([wp.denormalized_profile()
                                               for wp in folds[fold_idx]])
        valid = self._denormalized_list_to_pool([wp.denormalized_profile()
                                                for wp in folds[(fold_idx+1) %
                                                num_folds]])
        train = []
        for i, fold in enumerate(folds):
            if i != fold_idx and i != (fold_idx+1) % 10:
                train += [wp.denormalized_profile() for wp in fold]
        train = self._denormalized_list_to_pool(train)
        return test, valid, train


    def _divide_folds(self, seed, num_folds):
        """
        Return ``num_folds`` denormalized profiles, each containing approximately
        ``1/num_folds`` of this `DataPool`'s data.
        """
        r=RandomState(seed)
        remaining = [wp.denormalized_profile() for wp in self._weighted_profiles]
        folds = []
        for fold_idx in xrange(num_folds):
            fold = self._blank_denormalized()
            n = int(self.n) / int(num_folds)
            if fold_idx < int(self.n) % int(num_folds):
                n += 1
            self._select_points(r, fold, remaining, n)
            folds.append(fold)
        return folds

    def _divide_folds_gamewise(self, num_folds,
                               seed = None, stratified=False):
        r = RandomState(seed)
        games = self._generate_game_dictionary()
        game_idx = games.keys()
        n = len(game_idx)
        indices = range(n)
        r.shuffle(indices)

        if stratified:
            exp_lookup = self._experiment_lookup(games)
            fold_indices = [ [] for ix in xrange(num_folds) ]
            for stratum in exp_lookup.values():
                # [_split_indices_into_folds] puts "overflow" items in the
                # first folds, so sort emptier folds toward the beginning for balance.
                fold_indices.sort(key=len)
                stratum_indices = [i for i in indices if i in stratum]
                for i in stratum_indices:
                    indices.remove(i)
                stratum_folds = self._split_indices_into_folds(stratum_indices, num_folds)
                for ix in xrange(num_folds):
                    fold_indices[ix] += stratum_folds[ix]
        else:
            fold_indices = self._split_indices_into_folds(indices, num_folds)

        folds = []
        for fold_idx in fold_indices:
            profiles = []
            for idx in fold_idx:
                profiles = profiles + [wp for wp in games[game_idx[idx]]]
            folds.append(profiles)
        return folds

    def _split_indices_into_folds(self, indices, num_folds):
        n = len(indices)
        s = n/num_folds
        fold_indices = [list(indices)[i*s:(i+1)*s] for i in range(num_folds)] 
        for idx, i in enumerate(list(indices)[s*num_folds:]):
            fold_indices[idx] += [i]
        return fold_indices

    def _experiment_lookup(self, games):
        experiments = {}
        game_idx = games.keys()
        indices = array(range(len(game_idx)))
        for i in indices:
            exp_list = [g.game.title.split('.')[2]
                        for g in games[game_idx[i]]]
            for e in exp_list:
                experiments[e] = experiments.get(e, []) + [i]
        return experiments

    def _denormalized_list_to_pool(self, dnps):
        """
        Return a new DataPool specified by a list ``dnps`` of denormalized
        profiles.
        """
        wps = []
        for dnp in dnps:
            wps.append(WeightedUncorrelatedProfile(None, dnp))
        return DataPool(wps)

    def _blank_denormalized(self):
        """
        Return a list containing one empty denormalized profile for each weighted
        profile in this data pool.
        """
        dnps = [wp.denormalized_profile() for wp in self._weighted_profiles]
        for dnp in dnps:
            for i in xrange(len(dnp)):
                dnp[i] = 0.0
        return dnps

    def _generate_game_dictionary(self):
        """
        Generates a diction of games in the pool indexed by a tuple of 
        game payoffs
        """
        games = {}
        for wp in self._weighted_profiles:
            idx = tuple(a.payoff(player) for a in action_profiles(wp.game) for player in wp.game.players)
            games[idx] = games.get(idx, []) + [wp]
        return games

    def _select_points(self, rng, test, train, num_points):
        """
        Move ``num_points`` randomly-selected points from ``train`` to ``test``,
        where ``train`` and ``test`` are lists of denormalized profiles, using
        ``rng`` to generate random numbers.
        """
        # ??? Should we be operating on weighted profiles directly, in order to
        # better support ex_ante players?
        def select_point():
            point_idx = rng.randint(0, m)
            below = 0
            for (j, dnp) in enumerate(train):
                for (i, n) in enumerate(dnp):
                    below += n
                    if point_idx < below:
                        train[j][i] -= 1
                        test[j][i] += 1
                        return

        m = sum(sum(dnp) for dnp in train)
        for point_num in xrange(num_points):
            select_point()
            m -= 1

class WeightedUncorrelatedProfile(object):
    """
    A profile representing the empirical distribution of play in a single game, and a weight
    representing the number of independent observations in the empirical distribution.
    """
    def __init__(self, n, profile):
        """
        Pattern 1: Provide the total number of independent observations as ``n``
        and a normalized empirical profile as ``profile``.

        Pattern 2: Set ``n`` to `None` and provide a denormalized profile of
        counts as ``profile``.
        """
        self._profile=profile.copy();
        if n is None:
            self._n = None
        else:
            self._n=n

    def log_likelihood(self, prediction):
        """
        Return the log probability of the empirical distribution, assuming iid draws from
        'prediction'.  Log likelihoods are taken with respect to individual actions, not profiles;
        that is, there is no way to represent a correlated outcome.
        """
        ll = 0.0
        for (m,p) in zip(self.denormalized_profile(), prediction):
            if m > 0.0 and p > 0.0:
                try:
                    ll += m*math.log(p)
                except:
                    print "*** m=%s\tp=%s" % (m,p)
                    raise
            elif m > 0.0:
                # Zero-probability event occurred
                return -inf
        return ll

    @property
    def game(self):
        return self._profile.game

    def denormalized_profile(self):
        """
        Return a profile containing observation counts.
        """
        if self._n is None:
            return self._profile.copy()
        else:
            p = self._profile.copy()
            m = self._n / sum(p)
            for i in xrange(len(p)):
                p[i] *= m
                assert abs(p[i] - round(p[i])) < 1e-6
                p[i] = round(p[i])
            return p

    def normalized_profile(self):
        """
        Return a profile containing empirical frequencies.
        """
        if self._n is None:
            p = self._profile.copy()
            np = normalize(self._profile.copy())
            for i in xrange(len(p)):
                if p[i] == 0.0:
                    np[i] = 0.0
            return np
        else:
            return self._profile.copy()

    @property
    def n(self):
        if self._n is None:
            return sum(self._profile)
        else:
            return self._n

# Original versions of games
original_games = {}

def make_original(normalized_game, original_filename):
    """
    Update `original_games` to have an entry for ``normalized_game`` that
    points to a game loaded from ``original_filename``.
    """
    global original_games
    assert len(normalized_game.title) > 0
    g = gambit.read_game(original_filename)
    if normalized_game.title in original_games:
        assert repr(original_games[normalized_game.title]) == repr(g)
    else:
        original_games[normalized_game.title] = g

def original_game(game):
    global original_games
    if game.title in original_games:
        return original_games[game.title]
    else:
        return game


# ========================= Special-purpose overrides =========================

class AveragingPool(DataPool):
    def train_fold(self, seed, num_folds, fold_idx, return_both=False):
        if return_both:
            trn, tst = super(AveragingPool, self).train_fold(seed, num_folds, fold_idx, True)
            return AveragingPool(trn.weighted_profiles), AveragingPool(tst.weighted_profiles)
        else:
            trn = super(AveragingPool, self).train_fold(seed, num_folds, fold_idx, False)
            return AveragingPool(trn.weighted_profiles)

    def train_fold_gamewise(self, seed, num_folds, fold_idx,
                            return_both=False, stratified=False):
        if return_both:
            trn, tst = super(AveragingPool, self).train_fold_gamewise(seed, num_folds, fold_idx, True, stratified)
            return AveragingPool(trn.weighted_profiles), AveragingPool(tst.weighted_profiles)
        else:
            trn = super(AveragingPool, self).train_fold_gamewise(seed, num_folds, fold_idx, False, stratified)
            return AveragingPool(trn.weighted_profiles)

    def log_likelihood(self, set_predictor):
        """
        Given a callable 'predictor' that maps from a game to a set of predicted
        profiles of play, return the average log likelihood of the data pool's
        data given the predictions of `predictor`'s elements.
        """
        total_ll = 0.0

        for wp in self.weighted_profiles:
            eqa = set_predictor(wp.game)
            if len(eqa) == 1:
                total_ll += wp.log_likelihood(eqa[0])
            else:
                total_ll += (sum([ wp.log_likelihood(eqm) for eqm in eqa]) / float(len(eqa)))

        return total_ll

    def uniform_log_likelihood(self):
        """
        Return the log likelihood of this dataset according to a prediction that
        agents uniformly randomize over their actions.  (For normalization)
        """
        return self.log_likelihood(lambda g: [g.mixed_profile()])


class PeekabooPool(DataPool):
    def train_fold(self, seed, num_folds, fold_idx, return_both=False):
        if return_both:
            trn, tst = super(PeekabooPool, self).train_fold(seed, num_folds, fold_idx, True)
            return PeekabooPool(trn.weighted_profiles), PeekabooPool(tst.weighted_profiles)
        else:
            trn = super(PeekabooPool, self).train_fold(seed, num_folds, fold_idx, False)
            return PeekabooPool(trn.weighted_profiles)

    def train_fold_gamewise(self, seed, num_folds, fold_idx,
                            return_both=False, stratified=False):
        if return_both:
            trn, tst = super(PeekabooPool, self).train_fold_gamewise(seed, num_folds, fold_idx, True, stratified)
            return PeekabooPool(trn.weighted_profiles), PeekabooPool(tst.weighted_profiles)
        else:
            trn = super(PeekabooPool, self).train_fold_gamewise(seed, num_folds, fold_idx, False, stratified)
            return PeekabooPool(trn.weighted_profiles)

    def log_likelihood(self, predictor):
        """
        Given a callable 'predictor' that maps from a game to a predicted profile of play, return
        the log likelihood of the data pool's data given the predictions of 'predictor'.
        OVERRIDDEN: In this implementation, `predictor` gets to "peek" at the data that it will be applied to!
        """
        return sum([ wp.log_likelihood(predictor(wp.game, {'peek_data':wp})) for wp in self._weighted_profiles ])

    def uniform_log_likelihood(self):
        """
        Return the log likelihood of this dataset according to a prediction that
        agents uniformly randomize over their actions.  (For normalization)
        """
        return self.log_likelihood(lambda g, prediction_cache: g.mixed_profile())
