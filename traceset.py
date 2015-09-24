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

    def train_fold(self, fold_seed, num_folds, fold_idx, return_both=False):
        """
        Return the training fold for the specified fold_seed/num_folds/fold_idx.
        If 'return_both' is True, return the test fold as well.
        """
        r = np.random.RandomState(fold_seed)
        N = len(self.traceset)
        n = int(N) / int(num_folds)
        boundary = int(N) % int(num_folds)
        if fold_idx < boundary:
            n += 1
            s = n * fold_idx
        else:
            s = N - (n * (num_folds - fold_idx))

        indices = r.permutation(N)
        train = list(self.traceset)
        test = list([])
        for i in indices[s:s+n]:
            test.append(self.traceset[i])
            train.remove(self.traceset[i])

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

