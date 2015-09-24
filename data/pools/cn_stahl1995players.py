from bogota.datapool import DataPool, WeightedUncorrelatedProfile, make_profile
from gambit import Game
read_game = Game.read_game
import os.path
dirname=os.path.dirname(__file__)
cn_sw95_1=read_game(dirname+'/cn_sw95_1.nfg')
cn_sw95_2=read_game(dirname+'/cn_sw95_2.nfg')
cn_sw95_3=read_game(dirname+'/cn_sw95_3.nfg')
cn_sw95_4=read_game(dirname+'/cn_sw95_4.nfg')
cn_sw95_5=read_game(dirname+'/cn_sw95_5.nfg')
cn_sw95_6=read_game(dirname+'/cn_sw95_6.nfg')
cn_sw95_7=read_game(dirname+'/cn_sw95_7.nfg')
cn_sw95_8=read_game(dirname+'/cn_sw95_8.nfg')
cn_sw95_9=read_game(dirname+'/cn_sw95_9.nfg')
cn_sw95_10=read_game(dirname+'/cn_sw95_10.nfg')
cn_sw95_11=read_game(dirname+'/cn_sw95_11.nfg')
cn_sw95_12=read_game(dirname+'/cn_sw95_12.nfg')
cn_stahl1995players=DataPool(
    [WeightedUncorrelatedProfile(48,make_profile(cn_sw95_1,[0.14583333333333334,0.8333333333333334,0.020833333333333332,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(48,make_profile(cn_sw95_2,[0.625,0.25,0.125,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(48,make_profile(cn_sw95_3,[0.10416666666666667,0.3333333333333333,0.5625,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(48,make_profile(cn_sw95_4,[0.5416666666666666,0.3125,0.14583333333333334,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(48,make_profile(cn_sw95_5,[0.2916666666666667,0.0625,0.6458333333333334,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(48,make_profile(cn_sw95_6,[0.22916666666666666,0.4166666666666667,0.3541666666666667,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(48,make_profile(cn_sw95_7,[0.4375,0.3541666666666667,0.20833333333333334,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(48,make_profile(cn_sw95_8,[0.25,0.25,0.5,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(48,make_profile(cn_sw95_9,[0.5416666666666666,0.020833333333333332,0.4375,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(48,make_profile(cn_sw95_10,[0.8125,0.0625,0.125,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(48,make_profile(cn_sw95_11,[0.2708333333333333,0.08333333333333333,0.6458333333333334,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(48,make_profile(cn_sw95_12,[0.5416666666666666,0.0625,0.3958333333333333,0.0,0.0,0.0]))])
