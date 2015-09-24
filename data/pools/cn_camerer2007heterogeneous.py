from bogota.datapool import DataPool, WeightedUncorrelatedProfile, make_profile
from gambit import Game
read_game = Game.read_game
import os.path
dirname=os.path.dirname(__file__)
unprofitable=read_game(dirname+'/unprofitable.nfg')
cloned_matching_pennies=read_game(dirname+'/cloned_matching_pennies.nfg')
cloned_stag_hunt_hi=read_game(dirname+'/cloned_stag_hunt_hi.nfg')
cloned_stag_hunt_low=read_game(dirname+'/cloned_stag_hunt_low.nfg')
sw1=read_game(dirname+'/sw1.nfg')
sw2=read_game(dirname+'/sw2.nfg')
sw3=read_game(dirname+'/sw3.nfg')
sw4=read_game(dirname+'/sw4.nfg')
sw5=read_game(dirname+'/sw5.nfg')
sw6=read_game(dirname+'/sw6.nfg')
sw7=read_game(dirname+'/sw7.nfg')
sw8=read_game(dirname+'/sw8.nfg')
sw9=read_game(dirname+'/sw9.nfg')
sw10=read_game(dirname+'/sw10.nfg')
sw11=read_game(dirname+'/sw11.nfg')
sw12=read_game(dirname+'/sw12.nfg')
cloned_joker=read_game(dirname+'/cloned_joker.nfg')
cn_camerer2007heterogeneous=DataPool(
    [WeightedUncorrelatedProfile(74,make_profile(unprofitable,[0.32432432432432434,0.24324324324324326,0.43243243243243246,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(cloned_matching_pennies,[0.7837837837837838,0.10810810810810811,0.10810810810810811,0.7027027027027027,0.21621621621621623,0.08108108108108109])),
     WeightedUncorrelatedProfile(58,make_profile(cloned_stag_hunt_hi,[0.4482758620689655,0.3448275862068966,0.20689655172413793,0.896551724137931,0.10344827586206896])),
     WeightedUncorrelatedProfile(58,make_profile(cloned_stag_hunt_low,[0.2413793103448276,0.1724137931034483,0.5862068965517241,0.3448275862068966,0.6551724137931034])),
     WeightedUncorrelatedProfile(74,make_profile(sw1,[0.10810810810810811,0.8243243243243243,0.06756756756756757,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(sw2,[0.7972972972972973,0.14864864864864866,0.05405405405405406,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(sw3,[0.14864864864864866,0.17567567567567569,0.6756756756756757,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(sw4,[0.6081081081081081,0.35135135135135137,0.04054054054054054,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(sw5,[0.32432432432432434,0.28378378378378377,0.3918918918918919,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(sw6,[0.44594594594594594,0.25675675675675674,0.2972972972972973,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(sw7,[0.5945945945945946,0.12162162162162163,0.28378378378378377,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(sw8,[0.17567567567567569,0.20270270270270271,0.6216216216216216,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(sw9,[0.6486486486486487,0.04054054054054054,0.3108108108108108,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(sw10,[0.5135135135135135,0.1891891891891892,0.2972972972972973,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(sw11,[0.5,0.17567567567567569,0.32432432432432434,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(74,make_profile(sw12,[0.24324324324324326,0.17567567567567569,0.581081081081081,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cloned_joker,[0.06896551724137931,0.06896551724137931,0.1724137931034483,0.27586206896551724,0.41379310344827586,0.3793103448275862,0.3448275862068966,0.1724137931034483,0.10344827586206896]))])
