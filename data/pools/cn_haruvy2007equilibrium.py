from bogota.datapool import DataPool, WeightedUncorrelatedProfile, make_profile
from gambit import Game
read_game = Game.read_game
import os.path
dirname=os.path.dirname(__file__)
hs07_1=read_game(dirname+'/hs07_1.nfg')
hs07_2=read_game(dirname+'/hs07_2.nfg')
hs07_3=read_game(dirname+'/hs07_3.nfg')
hs07_4=read_game(dirname+'/hs07_4.nfg')
hs07_5=read_game(dirname+'/hs07_5.nfg')
hs07_6=read_game(dirname+'/hs07_6.nfg')
hs07_7=read_game(dirname+'/hs07_7.nfg')
hs07_8=read_game(dirname+'/hs07_8.nfg')
hs07_9=read_game(dirname+'/hs07_9.nfg')
hs07_10=read_game(dirname+'/hs07_10.nfg')
hs07_11=read_game(dirname+'/hs07_11.nfg')
hs07_12=read_game(dirname+'/hs07_12.nfg')
hs07_13=read_game(dirname+'/hs07_13.nfg')
hs07_14=read_game(dirname+'/hs07_14.nfg')
hs07_15=read_game(dirname+'/hs07_15.nfg')
hs07_16=read_game(dirname+'/hs07_16.nfg')
hs07_17=read_game(dirname+'/hs07_17.nfg')
hs07_18=read_game(dirname+'/hs07_18.nfg')
hs07_19=read_game(dirname+'/hs07_19.nfg')
hs07_20=read_game(dirname+'/hs07_20.nfg')
cn_haruvy2007equilibrium=DataPool(
    [WeightedUncorrelatedProfile(147,make_profile(hs07_1,[0.7891156462585034,0.047619047619047616,0.16326530612244897,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_2,[0.006802721088435374,0.06802721088435375,0.9251700680272109,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_3,[0.4421768707482993,0.5170068027210885,0.04081632653061224,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_4,[0.14285714285714285,0.8027210884353742,0.05442176870748299,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_5,[0.9115646258503401,0.027210884353741496,0.061224489795918366,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_6,[0.21768707482993196,0.034013605442176874,0.7482993197278912,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_7,[0.8435374149659864,0.034013605442176874,0.12244897959183673,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_8,[0.027210884353741496,0.9455782312925171,0.027210884353741496,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_9,[0.8163265306122449,0.1292517006802721,0.05442176870748299,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_10,[0.02040816326530612,0.047619047619047616,0.9319727891156463,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_11,[0.6666666666666666,0.3129251700680272,0.02040816326530612,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_12,[0.6530612244897959,0.08843537414965986,0.2585034013605442,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_13,[0.6938775510204082,0.10204081632653061,0.20408163265306123,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_14,[0.027210884353741496,0.8707482993197279,0.10204081632653061,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_15,[0.2925170068027211,0.5238095238095238,0.1836734693877551,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_16,[0.7482993197278912,0.14965986394557823,0.10204081632653061,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_17,[0.027210884353741496,0.06802721088435375,0.9047619047619048,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_18,[0.4897959183673469,0.19047619047619047,0.3197278911564626,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_19,[0.19727891156462585,0.6598639455782312,0.14285714285714285,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(147,make_profile(hs07_20,[0.013605442176870748,0.07482993197278912,0.9115646258503401,0.0,0.0,0.0]))])
