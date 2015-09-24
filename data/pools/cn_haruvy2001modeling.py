from bogota.datapool import DataPool, WeightedUncorrelatedProfile, make_profile
from gambit import Game
read_game = Game.read_game
import os.path
dirname=os.path.dirname(__file__)
cn_hsw01_1=read_game(dirname+'/cn_hsw01_1.nfg')
cn_hsw01_2=read_game(dirname+'/cn_hsw01_2.nfg')
cn_hsw01_3=read_game(dirname+'/cn_hsw01_3.nfg')
cn_hsw01_4=read_game(dirname+'/cn_hsw01_4.nfg')
cn_hsw01_5=read_game(dirname+'/cn_hsw01_5.nfg')
cn_hsw01_6=read_game(dirname+'/cn_hsw01_6.nfg')
cn_hsw01_7=read_game(dirname+'/cn_hsw01_7.nfg')
cn_hsw01_8=read_game(dirname+'/cn_hsw01_8.nfg')
cn_hsw01_9=read_game(dirname+'/cn_hsw01_9.nfg')
cn_hsw01_10=read_game(dirname+'/cn_hsw01_10.nfg')
cn_hsw01_11=read_game(dirname+'/cn_hsw01_11.nfg')
cn_hsw01_12=read_game(dirname+'/cn_hsw01_12.nfg')
cn_hsw01_13=read_game(dirname+'/cn_hsw01_13.nfg')
cn_hsw01_14=read_game(dirname+'/cn_hsw01_14.nfg')
cn_hsw01_15=read_game(dirname+'/cn_hsw01_15.nfg')
cn_haruvy2001modeling=DataPool(
    [WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_1,[0.43103448275862066,0.5689655172413793,0.0,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_2,[0.25862068965517243,0.5344827586206896,0.20689655172413793,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_3,[0.25862068965517243,0.4827586206896552,0.25862068965517243,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_4,[0.5,0.1724137931034483,0.3275862068965517,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_5,[0.7758620689655172,0.1724137931034483,0.05172413793103448,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(57,make_profile(cn_hsw01_6,[0.49122807017543857,0.07017543859649122,0.43859649122807015,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_7,[0.5344827586206896,0.13793103448275862,0.3275862068965517,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_8,[0.46551724137931033,0.15517241379310345,0.3793103448275862,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_9,[0.05172413793103448,0.2413793103448276,0.7068965517241379,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_10,[0.5517241379310345,0.20689655172413793,0.2413793103448276,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_11,[0.25862068965517243,0.603448275862069,0.13793103448275862,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_12,[0.603448275862069,0.05172413793103448,0.3448275862068966,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_13,[0.22413793103448276,0.1724137931034483,0.603448275862069,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_14,[0.5689655172413793,0.034482758620689655,0.39655172413793105,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(58,make_profile(cn_hsw01_15,[0.29310344827586204,0.034482758620689655,0.6724137931034483,0.0,0.0,0.0]))])
