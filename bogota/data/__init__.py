from bogota.datapool import DataPool
from bogota.traceset import TraceSet

import pools.cn_some9
cn_some9 = pools.cn_some9.cn_some9
cn_some8 = pools.cn_some9.cn_some8

import pools.cn_stahl1994experimental
cn_stahl1994experimental = pools.cn_stahl1994experimental.cn_stahl1994experimental

import pools.cn_stahl1995players
cn_stahl1995players = pools.cn_stahl1995players.cn_stahl1995players

import pools.cn_costagomes1998cognition
cn_costagomes1998cognition = pools.cn_costagomes1998cognition.cn_costagomes1998cognition
cn_costagomes1998cognition_traces = pools.cn_costagomes1998cognition.cn_costagomes1998cognition_traces

import pools.cn_goeree2001ten
cn_goeree2001ten = pools.cn_goeree2001ten.cn_goeree2001ten
cn_gh01_treasure = pools.cn_goeree2001ten.cn_gh01_treasure
cn_gh01_contra = pools.cn_goeree2001ten.cn_gh01_contra

import pools.cn_haruvy2001modeling
cn_haruvy2001modeling = pools.cn_haruvy2001modeling.cn_haruvy2001modeling

import pools.cn_cooper2003evidence
cn_cooper2003evidence = pools.cn_cooper2003evidence.cn_cooper2003evidence

import pools.cn_haruvy2007equilibrium
cn_haruvy2007equilibrium = pools.cn_haruvy2007equilibrium.cn_haruvy2007equilibrium

import pools.cn_stahl2008leveln
cn_stahl2008leveln = pools.cn_stahl2008leveln.cn_stahl2008leveln

import pools.cn_camerer2007heterogeneous
cn_camerer2007heterogeneous = pools.cn_camerer2007heterogeneous.cn_camerer2007heterogeneous

import pools.cn_costagomes2008stated
cn_costagomes2008stated = pools.cn_costagomes2008stated.cn_costagomes2008stated
cn_costagomes2008stated_traces = pools.cn_costagomes2008stated.cn_costagomes2008stated_traces

import pools.cn_costagomes2006cognition
cn_costagomes2006cognition_bin10 = pools.cn_costagomes2006cognition.cn_costagomes2006cognition_bin10
cn_costagomes2006cognition_bin10_traces = pools.cn_costagomes2006cognition.cn_costagomes2006cognition_bin10_traces
cn_costagomes2006cognition_bin25 = pools.cn_costagomes2006cognition.cn_costagomes2006cognition_bin25
cn_costagomes2006cognition_bin25_traces = pools.cn_costagomes2006cognition.cn_costagomes2006cognition_bin25_traces

cn_all9 = DataPool(cn_stahl1994experimental.weighted_profiles +
                   cn_stahl1995players.weighted_profiles +
                   cn_costagomes1998cognition.weighted_profiles +
                   cn_goeree2001ten.weighted_profiles +
                   cn_haruvy2001modeling.weighted_profiles +
                   cn_cooper2003evidence.weighted_profiles +
                   cn_haruvy2007equilibrium.weighted_profiles +
                   cn_stahl2008leveln.weighted_profiles +
                   cn_camerer2007heterogeneous.weighted_profiles)

cn_all10 = DataPool(cn_stahl1994experimental.weighted_profiles +
                    cn_stahl1995players.weighted_profiles +
                    cn_costagomes1998cognition.weighted_profiles +
                    cn_goeree2001ten.weighted_profiles +
                    cn_haruvy2001modeling.weighted_profiles +
                    cn_cooper2003evidence.weighted_profiles +
                    cn_haruvy2007equilibrium.weighted_profiles +
                    cn_stahl2008leveln.weighted_profiles +
                    cn_camerer2007heterogeneous.weighted_profiles +
                    cn_costagomes2008stated.weighted_profiles)

cn_all9_plusbinned = DataPool(cn_stahl1994experimental.weighted_profiles +
                    cn_stahl1995players.weighted_profiles +
                    cn_costagomes1998cognition.weighted_profiles +
                    cn_goeree2001ten.weighted_profiles +
                    cn_haruvy2001modeling.weighted_profiles +
                    cn_cooper2003evidence.weighted_profiles +
                    cn_haruvy2007equilibrium.weighted_profiles +
                    cn_stahl2008leveln.weighted_profiles +
                    cn_camerer2007heterogeneous.weighted_profiles +
                    cn_costagomes2006cognition_bin25.weighted_profiles)

cn_all11 = DataPool(cn_stahl1994experimental.weighted_profiles +
                    cn_stahl1995players.weighted_profiles +
                    cn_costagomes1998cognition.weighted_profiles +
                    cn_goeree2001ten.weighted_profiles +
                    cn_haruvy2001modeling.weighted_profiles +
                    cn_cooper2003evidence.weighted_profiles +
                    cn_haruvy2007equilibrium.weighted_profiles +
                    cn_stahl2008leveln.weighted_profiles +
                    cn_camerer2007heterogeneous.weighted_profiles +
                    cn_costagomes2008stated.weighted_profiles +
                    cn_costagomes2006cognition_bin25.weighted_profiles)

cn_all_traces = TraceSet(list(cn_costagomes1998cognition_traces) +
                         list(cn_costagomes2008stated_traces) +
                         list(cn_costagomes2006cognition_bin25_traces))

cn_all_traces_pooled = DataPool(cn_costagomes1998cognition.weighted_profiles +
                                cn_costagomes2008stated.weighted_profiles +
                                cn_costagomes2006cognition_bin25.weighted_profiles)
