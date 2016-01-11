from bogota.datapool import DataPool, WeightedUncorrelatedProfile, make_profile, read_and_cache_eqa
from bogota.traceset import TraceSet
read_game = read_and_cache_eqa
import os.path
dirname=os.path.dirname(__file__)
cn_cgcb2a=read_game(dirname+'/cn_cgcb2a.nfg')
cn_cgcb2b=read_game(dirname+'/cn_cgcb2b.nfg')
cn_cgcb3a=read_game(dirname+'/cn_cgcb3a.nfg')
cn_cgcb3b=read_game(dirname+'/cn_cgcb3b.nfg')
cn_cgcb4a=read_game(dirname+'/cn_cgcb4a.nfg')
cn_cgcb4b=read_game(dirname+'/cn_cgcb4b.nfg')
cn_cgcb4c=read_game(dirname+'/cn_cgcb4c.nfg')
cn_cgcb4d=read_game(dirname+'/cn_cgcb4d.nfg')
cn_cgcb5a=read_game(dirname+'/cn_cgcb5a.nfg')
cn_cgcb5b=read_game(dirname+'/cn_cgcb5b.nfg')
cn_cgcb6a=read_game(dirname+'/cn_cgcb6a.nfg')
cn_cgcb6b=read_game(dirname+'/cn_cgcb6b.nfg')
cn_cgcb7a=read_game(dirname+'/cn_cgcb7a.nfg')
cn_cgcb7b=read_game(dirname+'/cn_cgcb7b.nfg')
cn_cgcb8a=read_game(dirname+'/cn_cgcb8a.nfg')
cn_cgcb8b=read_game(dirname+'/cn_cgcb8b.nfg')
cn_cgcb9a=read_game(dirname+'/cn_cgcb9a.nfg')
cn_cgcb9b=read_game(dirname+'/cn_cgcb9b.nfg')
cn_costagomes1998cognition=DataPool(
    [WeightedUncorrelatedProfile(72,make_profile(cn_cgcb2a,[0.75,0.25,0.5833333333333334,0.4166666666666667])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb2b,[0.9166666666666666,0.08333333333333333,0.7222222222222222,0.2777777777777778])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb3a,[0.6944444444444444,0.3055555555555556,0.9166666666666666,0.08333333333333333])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb3b,[0.7222222222222222,0.2777777777777778,0.9444444444444444,0.05555555555555555])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb4a,[0.6944444444444444,0.3055555555555556,0.8611111111111112,0.0,0.1388888888888889])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb4b,[0.3888888888888889,0.05555555555555555,0.5555555555555556,0.8888888888888888,0.1111111111111111])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb4c,[0.9166666666666666,0.0,0.08333333333333333,0.5555555555555556,0.4444444444444444])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb4d,[0.8888888888888888,0.1111111111111111,0.7777777777777778,0.027777777777777776,0.19444444444444445])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb5a,[0.16666666666666666,0.027777777777777776,0.8055555555555556,0.5833333333333334,0.4166666666666667])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb5b,[0.1111111111111111,0.1388888888888889,0.75,0.6944444444444444,0.3055555555555556])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb6a,[0.6944444444444444,0.3055555555555556,0.16666666666666666,0.05555555555555555,0.7777777777777778])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb6b,[0.6111111111111112,0.3888888888888889,0.16666666666666666,0.1111111111111111,0.7222222222222222])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb7a,[0.5277777777777778,0.4722222222222222,0.19444444444444445,0.08333333333333333,0.7222222222222222])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb7b,[0.5555555555555556,0.4444444444444444,0.19444444444444445,0.05555555555555555,0.75])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb8a,[0.25,0.08333333333333333,0.6666666666666666,0.4722222222222222,0.5277777777777778])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb8b,[0.2222222222222222,0.08333333333333333,0.6944444444444444,0.4722222222222222,0.5277777777777778])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb9a,[0.9166666666666666,0.0,0.0,0.08333333333333333,0.6388888888888888,0.3611111111111111])),
     WeightedUncorrelatedProfile(72,make_profile(cn_cgcb9b,[0.8333333333333334,0.16666666666666666,0.8611111111111112,0.0,0.0,0.1388888888888889]))])

cn_costagomes1998cognition_traces=TraceSet([
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["B"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["B"], cn_cgcb3b.strategies["B"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["B"], cn_cgcb4d.strategies["B"], cn_cgcb5a.strategies["T"], cn_cgcb5b.strategies["M"], cn_cgcb6a.strategies["B"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["T"], cn_cgcb8b.strategies["T"], cn_cgcb9a.strategies["B"], cn_cgcb9b.strategies["B"], ],
[cn_cgcb2a.strategies["B"], cn_cgcb2b.strategies["B"], cn_cgcb3a.strategies["B"], cn_cgcb3b.strategies["B"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["B"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["M"], cn_cgcb6a.strategies["B"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["M"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["B"], cn_cgcb9b.strategies["B"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["B"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["B"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["B"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["B"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["B"], cn_cgcb4a.strategies["B"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["B"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["M"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["T"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["B"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["B"], cn_cgcb2b.strategies["B"], cn_cgcb3a.strategies["B"], cn_cgcb3b.strategies["B"], cn_cgcb4a.strategies["B"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["B"], cn_cgcb4d.strategies["B"], cn_cgcb5a.strategies["M"], cn_cgcb5b.strategies["T"], cn_cgcb6a.strategies["B"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["M"], cn_cgcb8b.strategies["M"], cn_cgcb9a.strategies["B"], cn_cgcb9b.strategies["B"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["T"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["T"], cn_cgcb8b.strategies["T"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["B"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["B"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["R"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["M"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["R"], cn_cgcb4b.strategies["R"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["M"], cn_cgcb7a.strategies["M"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["R"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["R"], cn_cgcb4a.strategies["R"], cn_cgcb4b.strategies["R"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["L"], cn_cgcb7a.strategies["L"], cn_cgcb7b.strategies["L"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["R"], cn_cgcb4b.strategies["R"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["R"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["R"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["L"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["L"], cn_cgcb7b.strategies["L"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["R"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["R"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["R"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["M"], cn_cgcb6b.strategies["M"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["R"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["R"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["R"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["R"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["R"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["L"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["B"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["B"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["M"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["B"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["B"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["B"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["B"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["B"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["T"], cn_cgcb8b.strategies["T"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["B"], cn_cgcb3a.strategies["B"], cn_cgcb3b.strategies["B"], cn_cgcb4a.strategies["B"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["B"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["M"], cn_cgcb8b.strategies["M"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["B"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["B"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["T"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["B"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["T"], cn_cgcb8b.strategies["T"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["B"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["B"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["T"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["B"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["B"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["B"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["R"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["R"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["L"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["R"], cn_cgcb3a.strategies["R"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["R"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["R"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["L"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["M"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["R"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["L"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["R"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["L"], cn_cgcb7b.strategies["L"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["R"], cn_cgcb3a.strategies["R"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["M"], cn_cgcb6b.strategies["M"], cn_cgcb7a.strategies["M"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["R"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["R"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["R"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["B"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["B"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["B"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["T"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["T"], cn_cgcb5b.strategies["T"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["T"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["M"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["T"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["T"], cn_cgcb8b.strategies["T"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["T"], cn_cgcb5b.strategies["T"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["T"], cn_cgcb8b.strategies["T"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["B"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["B"], cn_cgcb3b.strategies["B"], cn_cgcb4a.strategies["B"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["B"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["B"], ],
[cn_cgcb2a.strategies["B"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["B"], cn_cgcb3b.strategies["B"], cn_cgcb4a.strategies["B"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["M"], cn_cgcb6a.strategies["B"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["B"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["M"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["T"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["T"], cn_cgcb8b.strategies["T"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["T"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["B"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["T"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["T"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["T"], cn_cgcb2b.strategies["T"], cn_cgcb3a.strategies["T"], cn_cgcb3b.strategies["B"], cn_cgcb4a.strategies["T"], cn_cgcb4b.strategies["B"], cn_cgcb4c.strategies["T"], cn_cgcb4d.strategies["T"], cn_cgcb5a.strategies["B"], cn_cgcb5b.strategies["M"], cn_cgcb6a.strategies["T"], cn_cgcb6b.strategies["B"], cn_cgcb7a.strategies["T"], cn_cgcb7b.strategies["B"], cn_cgcb8a.strategies["B"], cn_cgcb8b.strategies["B"], cn_cgcb9a.strategies["T"], cn_cgcb9b.strategies["T"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["R"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["M"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["R"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["R"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["R"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["R"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["R"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["L"], cn_cgcb6b.strategies["M"], cn_cgcb7a.strategies["L"], cn_cgcb7b.strategies["L"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["M"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["R"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["L"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["R"], cn_cgcb6a.strategies["L"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["L"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["R"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["R"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["R"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["R"], cn_cgcb6a.strategies["L"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["L"], cn_cgcb6b.strategies["L"], cn_cgcb7a.strategies["L"], cn_cgcb7b.strategies["L"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["R"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["R"], cn_cgcb5a.strategies["R"], cn_cgcb5b.strategies["R"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["L"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["L"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["R"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["R"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["R"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["R"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["R"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["R"], cn_cgcb9b.strategies["L"], ],
[cn_cgcb2a.strategies["L"], cn_cgcb2b.strategies["L"], cn_cgcb3a.strategies["L"], cn_cgcb3b.strategies["L"], cn_cgcb4a.strategies["L"], cn_cgcb4b.strategies["L"], cn_cgcb4c.strategies["L"], cn_cgcb4d.strategies["L"], cn_cgcb5a.strategies["L"], cn_cgcb5b.strategies["L"], cn_cgcb6a.strategies["L"], cn_cgcb6b.strategies["R"], cn_cgcb7a.strategies["L"], cn_cgcb7b.strategies["R"], cn_cgcb8a.strategies["L"], cn_cgcb8b.strategies["R"], cn_cgcb9a.strategies["L"], cn_cgcb9b.strategies["L"], ],
])
