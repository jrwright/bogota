"""
Implement class for representing tracesets.
"""
import numpy as np

class TraceSet(object):
    """
    A traceset is a list of "traces".  A trace is a list of pure gambit
    strategies, representing a history of play by a single subject.
    """
    def __init__(self, list_of_traces):
        self.traceset = list_of_traces

    def __getitem__(self, idx):
        return self.traceset[idx]

    def _divide_folds(self, items, fold_seed, num_folds, fold_idx):
        r = np.random.RandomState(fold_seed)
        N = len(items)
        n = int(N) / int(num_folds)
        boundary = int(N) % int(num_folds)
        if fold_idx < boundary:
            n += 1
            s = n * fold_idx
        else:
            s = N - (n * (num_folds - fold_idx))

        indices = r.permutation(N)
        train = list(items)
        test = list([])
        for i in indices[s:s+n]:
            test.append(items[i])
            train.remove(items[i])

        return train,test

    def train_fold(self, fold_seed, num_folds, fold_idx, return_both=False, stratified=False):
        """
        Return the training fold for the specified fold_seed/num_folds/fold_idx.
        If 'return_both' is True, return the test fold as well.
        """
        assert stratified == False
        train, test = self._divide_folds(self.traceset, fold_seed, num_folds, fold_idx)

        if return_both:
            return TraceSet(train), TraceSet(test)
        else:
            return TraceSet(train)

    def train_fold_gamewise(self, fold_seed, num_folds, fold_idx, return_both=False, stratified=False):
        """
        Divide by both subject and game.  The test set will contain neither games
        nor subjects from the training set.
        """
        assert stratified == False

        # Collect all the games
        gset = set()
        for tr in self.traceset:
            for ai in tr:
                gset.add(ai.player.game)
        gset = sorted(gset, key=repr)
        train_games, test_games = self._divide_folds(gset, fold_seed, num_folds, fold_idx)

        # Break every trace into a training portion and a testing portion
        train = []
        test = []
        for tr in self.traceset:
            trn_tr = [ai for ai in tr if ai.player.game in train_games]
            if len(trn_tr) > 0:
                train.append(trn_tr)
            tst_tr = [ai for ai in tr if ai.player.game in test_games]
            if len(tst_tr) > 0:
                test.append(tst_tr)

        if return_both:
            return TraceSet(train), TraceSet(test)
        else:
            return TraceSet(train)

    def log_likelihood(self, trace_ll):
        """
        Given a callable 'trace_ll' function that maps from a trace to its
        log-likelihood, return the log likelihood of the full traceset.
        """
        prediction_cache = {}
        LLs = [ trace_ll(tr, prediction_cache = prediction_cache) for tr in self.traceset ]
        return sum(LLs)

    def uniform_log_likelihood(self):
        """
        Return the log likelihood of this dataset according to a prediction that
        agents uniformly randomize over their actions.  (For normalization)
        """
        def uniform_trace_ll(tr, prediction_cache=None):
            return sum(-np.log(len(ai.player.strategies)) for ai in tr)
        return self.log_likelihood(uniform_trace_ll)

