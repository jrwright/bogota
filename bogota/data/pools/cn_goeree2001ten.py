from bogota.datapool import DataPool, WeightedUncorrelatedProfile, make_profile, read_and_cache_eqa
read_game = read_and_cache_eqa
import os.path
dirname=os.path.dirname(__file__)

travellers_dilemma_low=read_game(dirname+'/travellers_dilemma_low.nfg')
travellers_dilemma_high=read_game(dirname+'/travellers_dilemma_high.nfg')

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
cn_goeree2001ten=DataPool(
    [WeightedUncorrelatedProfile(50,make_profile(travellers_dilemma_low,[0.08,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.02,0.0,0.0,0.0,0.0,0.0,0.04,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.02,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.04,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.02,0.0,0.0,0.0,0.0,0.02,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.02,0.02,0.0,0.02,0.02,0.18,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(50,make_profile(travellers_dilemma_high,[0.7599999999999998,0.019999999999999997,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.019999999999999997,0.0,0.019999999999999997,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.019999999999999997,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.019999999999999997,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.019999999999999997,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.019999999999999997,0.039999999999999994,0.059999999999999984,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(50,make_profile(matching_pennies_symmetric,[0.48,0.52,0.48,0.52])),
     WeightedUncorrelatedProfile(50,make_profile(matching_pennies_asymmetric,[0.96,0.04,0.16,0.84])),
     WeightedUncorrelatedProfile(50,make_profile(matching_pennies_asymmetric_reversed,[0.08,0.92,0.8,0.2])),
     WeightedUncorrelatedProfile(50,make_profile(kreps_basic,[0.68,0.32,0.24,0.08,0.68,0.0])),
     WeightedUncorrelatedProfile(50,make_profile(kreps_positive,[0.84,0.16,0.24,0.12,0.64,0.0])),
     WeightedUncorrelatedProfile(50,make_profile(kreps_treasure,[0.04,0.96,0.0,0.0,0.16,0.84])),
     WeightedUncorrelatedProfile(50,make_profile(minimum_effort_treasure,[0.08,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.04,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.02,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.1,0.0,0.02,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.08,0.0,0.0,0.0,0.0,0.02,0.0,0.0,0.0,0.0,0.04,0.0,0.0,0.0,0.02,0.0,0.0,0.0,0.0,0.0,0.58,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])),
     WeightedUncorrelatedProfile(50,make_profile(minimum_effort_contradiction,[0.38,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.12,0.0,0.02,0.0,0.02,0.02,0.0,0.0,0.0,0.0,0.12,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.06,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.08,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.04,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.14,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]))])

cn_gh01_treasure = DataPool([cn_goeree2001ten.weighted_profiles[1],
                              cn_goeree2001ten.weighted_profiles[2],
                              cn_goeree2001ten.weighted_profiles[7],
                              cn_goeree2001ten.weighted_profiles[8]])
cn_gh01_contra = DataPool([cn_goeree2001ten.weighted_profiles[0],
                           cn_goeree2001ten.weighted_profiles[3],
                           cn_goeree2001ten.weighted_profiles[4],
                           cn_goeree2001ten.weighted_profiles[5],
                           cn_goeree2001ten.weighted_profiles[6],
                           cn_goeree2001ten.weighted_profiles[9]])
