from bogota.datapool import DataPool, WeightedUncorrelatedProfile, make_profile
from gambit import Game
read_game = Game.read_game
import os.path
dirname=os.path.dirname(__file__)
sh08_1=read_game(dirname+'/sh08_1.nfg')
sh08_2=read_game(dirname+'/sh08_2.nfg')
sh08_3=read_game(dirname+'/sh08_3.nfg')
sh08_4=read_game(dirname+'/sh08_4.nfg')
sh08_5=read_game(dirname+'/sh08_5.nfg')
sh08_6=read_game(dirname+'/sh08_6.nfg')
sh08_7=read_game(dirname+'/sh08_7.nfg')
sh08_8=read_game(dirname+'/sh08_8.nfg')
sh08_9=read_game(dirname+'/sh08_9.nfg')
sh08_10=read_game(dirname+'/sh08_10.nfg')
sh08_11=read_game(dirname+'/sh08_11.nfg')
sh08_12=read_game(dirname+'/sh08_12.nfg')
sh08_13=read_game(dirname+'/sh08_13.nfg')
sh08_14=read_game(dirname+'/sh08_14.nfg')
sh08_15=read_game(dirname+'/sh08_15.nfg')
sh08_16=read_game(dirname+'/sh08_16.nfg')
sh08_17=read_game(dirname+'/sh08_17.nfg')
sh08_18=read_game(dirname+'/sh08_18.nfg')
cn_stahl2008leveln=DataPool(
    [WeightedUncorrelatedProfile(75,make_profile(sh08_1,[0.3466666666666667,0.6533333333333333,0.0,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_2,[0.013333333333333334,0.48,0.5066666666666667,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_3,[0.8533333333333334,0.10666666666666667,0.04,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_4,[0.8266666666666667,0.16,0.013333333333333334,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_5,[0.7066666666666667,0.05333333333333334,0.24,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_6,[0.013333333333333334,0.5466666666666666,0.44,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_7,[0.48,0.013333333333333334,0.5066666666666667,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_8,[0.0,0.56,0.44,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_9,[0.5866666666666667,0.36,0.05333333333333334,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(97,make_profile(sh08_10,[0.12371134020618557,0.6494845360824743,0.2268041237113402,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_11,[0.22666666666666666,0.6933333333333334,0.08,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_12,[0.72,0.0,0.28,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_13,[0.52,0.18666666666666668,0.29333333333333333,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_14,[0.013333333333333334,0.5733333333333334,0.41333333333333333,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(75,make_profile(sh08_15,[0.4,0.5866666666666667,0.013333333333333334,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(47,make_profile(sh08_16,[0.7659574468085106,0.23404255319148937,0.0,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(47,make_profile(sh08_17,[0.0,0.6170212765957447,0.3829787234042553,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(47,make_profile(sh08_18,[0.2765957446808511,0.0,0.723404255319149,0.0,0.0,0.0]))])
