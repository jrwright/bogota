import csv
import glob
import gambit
from bogota.data import cn_all11, cn_costagomes2006cognition_bin10

def sanity_check():
    for fname in glob.glob("*.nfg"):
        g = gambit.Game.read_game(fname)
        stem = g.title[g.title.rindex('.')+1:]
        assert fname == stem+'.nfg', (fname, stem)


def main():
    for wp in cn_all11.weighted_profiles + cn_costagomes2006cognition_bin10.weighted_profiles:
        stem = wp.game.title[wp.game.title.rindex('.')+1:]
        fname = stem + '.csv'
        dnp = wp.denormalized_profile()
        print """
if [ -e %s ]; then
  cp %s %s
fi
        """ % (stem[3:]+'.nfg', fname, stem[3:]+'.csv')
        with open(fname, 'wb') as f:
            w = csv.writer(f)
            for pl in dnp.game.players:
                w.writerow(dnp[pl])


if __name__ == '__main__':
    main()
