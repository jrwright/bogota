from bogota.datapool import DataPool, WeightedUncorrelatedProfile, make_profile, read_and_cache_eqa
from gambit import Game
read_game = read_and_cache_eqa
import os.path
dirname=os.path.dirname(__file__)
cn_cvh03_1=read_game(dirname+'/cn_cvh03_1.nfg')
cn_cvh03_2=read_game(dirname+'/cn_cvh03_2.nfg')
cn_cvh03_3=read_game(dirname+'/cn_cvh03_3.nfg')
cn_cvh03_4=read_game(dirname+'/cn_cvh03_4.nfg')
cn_cvh03_5=read_game(dirname+'/cn_cvh03_5.nfg')
cn_cvh03_6=read_game(dirname+'/cn_cvh03_6.nfg')
cn_cvh03_7=read_game(dirname+'/cn_cvh03_7.nfg')
cn_cvh03_8=read_game(dirname+'/cn_cvh03_8.nfg')
cn_cooper2003evidence=DataPool(
    [WeightedUncorrelatedProfile(374,make_profile(cn_cvh03_1,[0.3155080213903743,0.6844919786096256,0.28342245989304815,0.7165775401069518])),
     WeightedUncorrelatedProfile(374,make_profile(cn_cvh03_2,[0.9090909090909091,0.09090909090909091,0.7379679144385026,0.2620320855614973])),
     WeightedUncorrelatedProfile(374,make_profile(cn_cvh03_3,[0.5828877005347594,0.41711229946524064,0.40106951871657753,0.5989304812834224])),
     WeightedUncorrelatedProfile(374,make_profile(cn_cvh03_4,[0.5775401069518716,0.42245989304812837,0.9197860962566845,0.08021390374331551])),
     WeightedUncorrelatedProfile(374,make_profile(cn_cvh03_5,[0.27807486631016043,0.7219251336898396,0.6737967914438503,0.32620320855614976])),
     WeightedUncorrelatedProfile(374,make_profile(cn_cvh03_6,[0.37967914438502676,0.6203208556149733,0.893048128342246,0.10695187165775401])),
     WeightedUncorrelatedProfile(374,make_profile(cn_cvh03_7,[0.37433155080213903,0.6256684491978609,0.18716577540106952,0.8128342245989305])),
     WeightedUncorrelatedProfile(374,make_profile(cn_cvh03_8,[0.732620320855615,0.26737967914438504,0.8609625668449198,0.13903743315508021]))])
