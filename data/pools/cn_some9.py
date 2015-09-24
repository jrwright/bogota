from bogota.datapool import DataPool, WeightedUncorrelatedProfile, make_profile, make_original
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
cn_cgcb2a=read_game(dirname+'/cn_cgcb2a.nfg')
make_original(cn_cgcb2a, dirname+'/cgcb2a.nfg')
cn_cgcb2b=read_game(dirname+'/cn_cgcb2b.nfg')
make_original(cn_cgcb2b, dirname+'/cgcb2b.nfg')
cn_cgcb3a=read_game(dirname+'/cn_cgcb3a.nfg')
make_original(cn_cgcb3a, dirname+'/cgcb3a.nfg')
cn_cgcb3b=read_game(dirname+'/cn_cgcb3b.nfg')
make_original(cn_cgcb3b, dirname+'/cgcb3b.nfg')
cn_cgcb4a=read_game(dirname+'/cn_cgcb4a.nfg')
make_original(cn_cgcb4a, dirname+'/cgcb4a.nfg')
cn_cgcb4b=read_game(dirname+'/cn_cgcb4b.nfg')
make_original(cn_cgcb4b, dirname+'/cgcb4b.nfg')
cn_cgcb4c=read_game(dirname+'/cn_cgcb4c.nfg')
make_original(cn_cgcb4c, dirname+'/cgcb4c.nfg')
cn_cgcb4d=read_game(dirname+'/cn_cgcb4d.nfg')
make_original(cn_cgcb4d, dirname+'/cgcb4d.nfg')
cn_cgcb5a=read_game(dirname+'/cn_cgcb5a.nfg')
make_original(cn_cgcb5a, dirname+'/cgcb5a.nfg')
cn_cgcb5b=read_game(dirname+'/cn_cgcb5b.nfg')
make_original(cn_cgcb5b, dirname+'/cgcb5b.nfg')
cn_cgcb6a=read_game(dirname+'/cn_cgcb6a.nfg')
make_original(cn_cgcb6a, dirname+'/cgcb6a.nfg')
cn_cgcb6b=read_game(dirname+'/cn_cgcb6b.nfg')
make_original(cn_cgcb6b, dirname+'/cgcb6b.nfg')
cn_cgcb7a=read_game(dirname+'/cn_cgcb7a.nfg')
make_original(cn_cgcb7a, dirname+'/cgcb7a.nfg')
cn_cgcb7b=read_game(dirname+'/cn_cgcb7b.nfg')
make_original(cn_cgcb7b, dirname+'/cgcb7b.nfg')
cn_cgcb8a=read_game(dirname+'/cn_cgcb8a.nfg')
make_original(cn_cgcb8a, dirname+'/cgcb8a.nfg')
cn_cgcb8b=read_game(dirname+'/cn_cgcb8b.nfg')
make_original(cn_cgcb8b, dirname+'/cgcb8b.nfg')
cn_cgcb9a=read_game(dirname+'/cn_cgcb9a.nfg')
make_original(cn_cgcb9a, dirname+'/cgcb9a.nfg')
cn_cgcb9b=read_game(dirname+'/cn_cgcb9b.nfg')
make_original(cn_cgcb9b, dirname+'/cgcb9b.nfg')

travellers_dilemma_low=read_game(dirname+'/travellers_dilemma_low.agg')
travellers_dilemma_high=read_game(dirname+'/travellers_dilemma_high.agg')

# Add back metadata that doesn't persist through the file format
travellers_dilemma_low.title = "bogota.data.cn_goeree2001ten.travellers_dilemma_low"
for i in xrange(300, 180-1, -1): # Descending order to avoid name collisions
    travellers_dilemma_low.players[0].strategies[i-180].label=str(i)
    travellers_dilemma_low.players[1].strategies[i-180].label=str(i)
travellers_dilemma_high.title = "bogota.data.cn_goeree2001ten.travellers_dilemma_high"
for i in xrange(300, 180-1, -1):
    travellers_dilemma_high.players[0].strategies[i-180].label=str(i)
    travellers_dilemma_high.players[1].strategies[i-180].label=str(i)

matching_pennies_symmetric=read_game(dirname+'/matching_pennies_symmetric.nfg')
matching_pennies_asymmetric=read_game(dirname+'/matching_pennies_asymmetric.nfg')
matching_pennies_asymmetric_reversed=read_game(dirname+'/matching_pennies_asymmetric_reversed.nfg')
kreps_basic=read_game(dirname+'/kreps_basic.nfg')
kreps_positive=read_game(dirname+'/kreps_positive.nfg')
kreps_treasure=read_game(dirname+'/kreps_treasure.nfg')
minimum_effort_treasure=read_game(dirname+'/minimum_effort_treasure.nfg')
minimum_effort_contradiction=read_game(dirname+'/minimum_effort_contradiction.nfg')
cn_sw94_1=read_game(dirname+'/cn_sw94_1.nfg')
make_original(cn_sw94_1, dirname+'/sw94_1.nfg')
cn_sw94_2=read_game(dirname+'/cn_sw94_2.nfg')
make_original(cn_sw94_2, dirname+'/sw94_2.nfg')
cn_sw94_3=read_game(dirname+'/cn_sw94_3.nfg')
make_original(cn_sw94_3, dirname+'/sw94_3.nfg')
cn_sw94_4=read_game(dirname+'/cn_sw94_4.nfg')
make_original(cn_sw94_4, dirname+'/sw94_4.nfg')
cn_sw94_5=read_game(dirname+'/cn_sw94_5.nfg')
make_original(cn_sw94_5, dirname+'/sw94_5.nfg')
cn_sw94_6=read_game(dirname+'/cn_sw94_6.nfg')
make_original(cn_sw94_6, dirname+'/sw94_6.nfg')
cn_sw94_7=read_game(dirname+'/cn_sw94_7.nfg')
make_original(cn_sw94_7, dirname+'/sw94_7.nfg')
cn_sw94_8=read_game(dirname+'/cn_sw94_8.nfg')
make_original(cn_sw94_8, dirname+'/sw94_8.nfg')
cn_sw94_9=read_game(dirname+'/cn_sw94_9.nfg')
make_original(cn_sw94_9, dirname+'/sw94_9.nfg')
cn_sw94_10=read_game(dirname+'/cn_sw94_10.nfg')
make_original(cn_sw94_10, dirname+'/sw94_10.nfg')
cn_sw95_1=read_game(dirname+'/cn_sw95_1.nfg')
make_original(cn_sw95_1, dirname+'/sw95_1.nfg')
cn_sw95_2=read_game(dirname+'/cn_sw95_2.nfg')
make_original(cn_sw95_2, dirname+'/sw95_2.nfg')
cn_sw95_3=read_game(dirname+'/cn_sw95_3.nfg')
make_original(cn_sw95_3, dirname+'/sw95_3.nfg')
cn_sw95_4=read_game(dirname+'/cn_sw95_4.nfg')
make_original(cn_sw95_4, dirname+'/sw95_4.nfg')
cn_sw95_5=read_game(dirname+'/cn_sw95_5.nfg')
make_original(cn_sw95_5, dirname+'/sw95_5.nfg')
cn_sw95_6=read_game(dirname+'/cn_sw95_6.nfg')
make_original(cn_sw95_6, dirname+'/sw95_6.nfg')
cn_sw95_7=read_game(dirname+'/cn_sw95_7.nfg')
make_original(cn_sw95_7, dirname+'/sw95_7.nfg')
cn_sw95_8=read_game(dirname+'/cn_sw95_8.nfg')
make_original(cn_sw95_8, dirname+'/sw95_8.nfg')
cn_sw95_9=read_game(dirname+'/cn_sw95_9.nfg')
make_original(cn_sw95_9, dirname+'/sw95_9.nfg')
cn_sw95_10=read_game(dirname+'/cn_sw95_10.nfg')
make_original(cn_sw95_10, dirname+'/sw95_10.nfg')
cn_sw95_11=read_game(dirname+'/cn_sw95_11.nfg')
make_original(cn_sw95_11, dirname+'/sw95_11.nfg')
cn_sw95_12=read_game(dirname+'/cn_sw95_12.nfg')
make_original(cn_sw95_12, dirname+'/sw95_12.nfg')
cn_cvh03_1=read_game(dirname+'/cn_cvh03_1.nfg')
make_original(cn_cvh03_1, dirname+'/cvh03_1.nfg')
cn_cvh03_2=read_game(dirname+'/cn_cvh03_2.nfg')
make_original(cn_cvh03_2, dirname+'/cvh03_2.nfg')
cn_cvh03_3=read_game(dirname+'/cn_cvh03_3.nfg')
make_original(cn_cvh03_3, dirname+'/cvh03_3.nfg')
cn_cvh03_4=read_game(dirname+'/cn_cvh03_4.nfg')
make_original(cn_cvh03_4, dirname+'/cvh03_4.nfg')
cn_cvh03_5=read_game(dirname+'/cn_cvh03_5.nfg')
make_original(cn_cvh03_5, dirname+'/cvh03_5.nfg')
cn_cvh03_6=read_game(dirname+'/cn_cvh03_6.nfg')
make_original(cn_cvh03_6, dirname+'/cvh03_6.nfg')
cn_cvh03_7=read_game(dirname+'/cn_cvh03_7.nfg')
make_original(cn_cvh03_7, dirname+'/cvh03_7.nfg')
cn_cvh03_8=read_game(dirname+'/cn_cvh03_8.nfg')
make_original(cn_cvh03_8, dirname+'/cvh03_8.nfg')
cn_hsw01_1=read_game(dirname+'/cn_hsw01_1.nfg')
make_original(cn_hsw01_1, dirname+'/hsw01_1.nfg')
cn_hsw01_2=read_game(dirname+'/cn_hsw01_2.nfg')
make_original(cn_hsw01_2, dirname+'/hsw01_2.nfg')
cn_hsw01_3=read_game(dirname+'/cn_hsw01_3.nfg')
make_original(cn_hsw01_3, dirname+'/hsw01_3.nfg')
cn_hsw01_4=read_game(dirname+'/cn_hsw01_4.nfg')
make_original(cn_hsw01_4, dirname+'/hsw01_4.nfg')
cn_hsw01_5=read_game(dirname+'/cn_hsw01_5.nfg')
make_original(cn_hsw01_5, dirname+'/hsw01_5.nfg')
cn_hsw01_6=read_game(dirname+'/cn_hsw01_6.nfg')
make_original(cn_hsw01_6, dirname+'/hsw01_6.nfg')
cn_hsw01_7=read_game(dirname+'/cn_hsw01_7.nfg')
make_original(cn_hsw01_7, dirname+'/hsw01_7.nfg')
cn_hsw01_8=read_game(dirname+'/cn_hsw01_8.nfg')
make_original(cn_hsw01_8, dirname+'/hsw01_8.nfg')
cn_hsw01_9=read_game(dirname+'/cn_hsw01_9.nfg')
make_original(cn_hsw01_9, dirname+'/hsw01_9.nfg')
cn_hsw01_10=read_game(dirname+'/cn_hsw01_10.nfg')
make_original(cn_hsw01_10, dirname+'/hsw01_10.nfg')
cn_hsw01_11=read_game(dirname+'/cn_hsw01_11.nfg')
make_original(cn_hsw01_11, dirname+'/hsw01_11.nfg')
cn_hsw01_12=read_game(dirname+'/cn_hsw01_12.nfg')
make_original(cn_hsw01_12, dirname+'/hsw01_12.nfg')
cn_hsw01_13=read_game(dirname+'/cn_hsw01_13.nfg')
make_original(cn_hsw01_13, dirname+'/hsw01_13.nfg')
cn_hsw01_14=read_game(dirname+'/cn_hsw01_14.nfg')
make_original(cn_hsw01_14, dirname+'/hsw01_14.nfg')
cn_hsw01_15=read_game(dirname+'/cn_hsw01_15.nfg')
make_original(cn_hsw01_15, dirname+'/hsw01_15.nfg')
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

_cpr07_wps=\
[WeightedUncorrelatedProfile(None,make_profile(unprofitable,[8, 8, 10, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cloned_matching_pennies,[15, 2, 3, 8, 2, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cloned_stag_hunt_hi,[4, 2, 4, 8, 1])),
 WeightedUncorrelatedProfile(None,make_profile(cloned_stag_hunt_low,[3, 2, 6, 4, 6])),
 WeightedUncorrelatedProfile(None,make_profile(sw1,[3, 16, 2, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sw2,[22, 5, 1, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sw3,[4, 2, 13, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sw4,[14, 8, 0, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sw5,[11, 6, 7, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sw6,[11, 7, 8, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sw7,[18, 2, 9, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sw8,[7, 4, 18, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sw9,[13, 0, 11, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sw10,[9, 2, 4, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sw11,[14, 3, 6, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sw12,[9, 1, 14, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cloned_joker,[1, 1, 0, 5, 2, 4, 4, 2, 1]))
]
_some8_wps=\
[ WeightedUncorrelatedProfile(None,make_profile(cn_cgcb2a,[12, 2, 10, 2])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb2b,[10, 0, 6, 1])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb3a,[11, 4, 12, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb3b,[8, 5, 10, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb4a,[5, 2, 11, 0, 3])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb4b,[3, 0, 6, 10, 1])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb4c,[9, 0, 1, 3, 8])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb4d,[13, 0, 6, 0, 2])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb5a,[3, 1, 13, 6, 6])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb5b,[1, 2, 7, 11, 4])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb6a,[8, 2, 2, 0, 12])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb6b,[7, 6, 1, 3, 7])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb7a,[9, 3, 1, 1, 8])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb7b,[4, 6, 3, 2, 12])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb8a,[3, 0, 7, 8, 3])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb8b,[4, 1, 4, 4, 5])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb9a,[6, 0, 0, 1, 9, 2])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cgcb9b,[3, 0, 10, 0, 0, 3])),
 WeightedUncorrelatedProfile(None,make_profile(travellers_dilemma_low,[4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 7, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(travellers_dilemma_high,[32, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(matching_pennies_symmetric,[10, 12, 11, 11])),
 WeightedUncorrelatedProfile(None,make_profile(matching_pennies_asymmetric,[15, 1, 3, 17])),
 WeightedUncorrelatedProfile(None,make_profile(matching_pennies_asymmetric_reversed,[2, 18, 19, 4])),
 WeightedUncorrelatedProfile(None,make_profile(kreps_basic,[13, 6, 3, 2, 13, 0])),
 WeightedUncorrelatedProfile(None,make_profile(kreps_positive,[13, 4, 6, 3, 14, 0])),
 WeightedUncorrelatedProfile(None,make_profile(kreps_treasure,[1, 21, 0, 0, 3, 20])),
 WeightedUncorrelatedProfile(None,make_profile(minimum_effort_treasure,[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(minimum_effort_contradiction,[13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 1, 0, 0, 1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw94_1,[11, 0, 29, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw94_2,[26, 7, 7, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw94_3,[14, 26, 0, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw94_4,[0, 27, 13, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw94_5,[18, 0, 22, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw94_6,[4, 35, 1, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw94_7,[6, 31, 3, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw94_8,[8, 13, 19, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw94_9,[26, 0, 14, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw94_10,[5, 0, 35, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_1,[4, 22, 1, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_2,[25, 6, 6, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_3,[4, 12, 20, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_4,[18, 9, 6, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_5,[9, 1, 20, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_6,[7, 14, 11, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_7,[16, 11, 9, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_8,[7, 8, 20, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_9,[18, 1, 16, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_10,[29, 3, 5, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_11,[6, 4, 20, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_sw95_12,[18, 3, 11, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cvh03_1,[8, 18, 5, 15])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cvh03_2,[24, 2, 17, 9])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cvh03_3,[23, 13, 7, 21])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cvh03_4,[16, 10, 17, 1])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cvh03_5,[9, 16, 16, 7])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cvh03_6,[14, 15, 21, 2])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cvh03_7,[10, 13, 4, 23])),
 WeightedUncorrelatedProfile(None,make_profile(cn_cvh03_8,[16, 5, 20, 3])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_1,[9, 15, 0, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_2,[5, 12, 6, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_3,[6, 12, 4, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_4,[12, 4, 7, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_5,[23, 7, 0, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_6,[17, 3, 14, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_7,[16, 1, 10, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_8,[10, 5, 10, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_9,[3, 5, 19, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_10,[19, 4, 6, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_11,[9, 20, 3, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_12,[17, 1, 8, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_13,[8, 6, 13, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_14,[14, 1, 12, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(cn_hsw01_15,[6, 1, 17, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_1,[13, 1, 7, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_2,[0, 1, 20, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_3,[7, 6, 1, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_4,[5, 17, 1, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_5,[21, 0, 2, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_6,[5, 0, 10, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_7,[23, 3, 5, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_8,[1, 14, 1, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_9,[18, 2, 1, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_10,[0, 0, 19, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_11,[12, 7, 1, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_12,[12, 1, 2, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_13,[15, 1, 5, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_14,[1, 23, 4, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_15,[6, 7, 6, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_16,[12, 5, 6, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_17,[1, 1, 17, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_18,[3, 3, 7, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_19,[4, 13, 2, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(hs07_20,[0, 2, 17, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_1,[12, 11, 0, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_2,[0, 7, 10, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_3,[16, 1, 3, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_4,[23, 4, 1, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_5,[10, 2, 5, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_6,[0, 8, 8, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_7,[12, 1, 11, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_8,[0, 16, 14, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_9,[10, 8, 2, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_10,[6, 23, 4, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_11,[3, 20, 2, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_12,[22, 0, 6, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_13,[11, 4, 6, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_14,[0, 15, 13, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_15,[7, 10, 0, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_16,[16, 4, 0, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_17,[0, 11, 6, 0, 0, 0])),
 WeightedUncorrelatedProfile(None,make_profile(sh08_18,[3, 0, 13, 0, 0, 0]))]

cn_some8=DataPool(_some8_wps) # Omit cpr07 as a testing set
cn_some9=DataPool(_cpr07_wps + _some8_wps)
