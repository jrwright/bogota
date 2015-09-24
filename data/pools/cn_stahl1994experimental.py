from bogota.datapool import DataPool, WeightedUncorrelatedProfile, make_profile
from gambit import Game
read_game = Game.read_game
import os.path
dirname=os.path.dirname(__file__)
cn_sw94_1=read_game(dirname+'/cn_sw94_1.nfg')
cn_sw94_2=read_game(dirname+'/cn_sw94_2.nfg')
cn_sw94_3=read_game(dirname+'/cn_sw94_3.nfg')
cn_sw94_4=read_game(dirname+'/cn_sw94_4.nfg')
cn_sw94_5=read_game(dirname+'/cn_sw94_5.nfg')
cn_sw94_6=read_game(dirname+'/cn_sw94_6.nfg')
cn_sw94_7=read_game(dirname+'/cn_sw94_7.nfg')
cn_sw94_8=read_game(dirname+'/cn_sw94_8.nfg')
cn_sw94_9=read_game(dirname+'/cn_sw94_9.nfg')
cn_sw94_10=read_game(dirname+'/cn_sw94_10.nfg')
cn_stahl1994experimental=DataPool(
    [WeightedUncorrelatedProfile(40,make_profile(cn_sw94_1,[0.275,0.0,0.725,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(40,make_profile(cn_sw94_2,[0.65,0.175,0.175,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(40,make_profile(cn_sw94_3,[0.35,0.65,0.0,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(40,make_profile(cn_sw94_4,[0.0,0.675,0.325,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(40,make_profile(cn_sw94_5,[0.45,0.0,0.55,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(40,make_profile(cn_sw94_6,[0.1,0.875,0.025,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(40,make_profile(cn_sw94_7,[0.15,0.775,0.075,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(40,make_profile(cn_sw94_8,[0.2,0.325,0.475,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(40,make_profile(cn_sw94_9,[0.65,0.0,0.35,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(40,make_profile(cn_sw94_10,[0.125,0.0,0.875,0.0,0.0,0.0]))])
