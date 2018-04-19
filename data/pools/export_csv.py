import csv
import glob
import gambit
from bogota.data import cn_all11, cn_costagomes2006cognition_bin10, cn_costagomes2008stated

def sanity_check():
    for fname in glob.glob("*.nfg"):
        g = gambit.Game.read_game(fname)
        stem = g.title[g.title.rindex('.')+1:]
        assert fname == stem+'.nfg', (fname, stem)


def export_cgw08(pool=cn_costagomes2008stated, row_actions=['T', 'M', 'B'], col_actions=['L', 'M', 'R'], norm=15./14):
    wp = pool.weighted_profiles[0]
    stem = wp.game.title[wp.game.title.rindex('.')+1:]
    stem = stem[len("cn_"):stem.rindex('_')]
    fname = stem + '-games.tex'

    sorted_profiles = sorted(pool.weighted_profiles, key=lambda wp:int(wp.game.title[wp.game.title.rindex('_')+1:]))
    

    with open(fname, 'wt') as out:
        for wp in sorted_profiles:
            assert len(wp.game.players) == 2

            n_row = len(wp.game.players[0].strategies)
            assert n_row == len(row_actions)
            n_col = len(wp.game.players[1].strategies)
            assert n_col == len(col_actions)

            # -game.tex
            name = wp.game.title[wp.game.title.rindex('.')+1:].replace("_", "-").upper()[len("cn_"):]
            out.write("\\subfigure[%s]{\n" % name)
            out.write("\\begin{game}{3}{3}\n")
            for head in col_actions:
                out.write(" \\> $%s$" % head)
            out.write(" \\\\\n")
            for i in xrange(n_row):
                out.write(" $%s$" % row_actions[i])
                for j in xrange(n_col):
                    out.write(" \\> $%d,%d$" % (float(wp.game[i,j][0])/norm, float(wp.game[i,j][1])/norm))
                if i < n_row-1:
                    out.write(" \\\\")
                out.write("\n")
            out.write("\\end{game}\n}\n")

    # -observations.csv
    fname = stem + '-observations.csv'
    with open(fname, 'wt') as out:
        for wp in sorted_profiles:
            name = wp.game.title[wp.game.title.rindex('.')+1:].replace("_", "-").upper()[len("cn_"):]
            dnp = wp.denormalized_profile()
            for i in xrange(n_row):
                out.write("%s,%s,%d,%s,%d\n" % (stem.upper(), name, 1, row_actions[i], dnp[wp.game.players[0]][i]))
            for j in xrange(n_col):
                out.write("%s,%s,%d,%s,%d\n" % (stem.upper(), name, 2, row_actions[j], dnp[wp.game.players[1]][j]))

    # -observations.tex
    fname = stem + '-observations.tex'
    with open(fname, 'wt') as out:
        for wp in sorted_profiles:
            name = wp.game.title[wp.game.title.rindex('.')+1:].replace("_", "-").upper()[len("cn_"):]
            col1 = "\\parbox[b]{2in}{%s}" % name
            for i in xrange(n_row):
                out.write(col1)
                col1 = "\\nopagebreak"
                out.write(" & $%s$ & $%2d$  & $%s$ & $%2d$ \\\\\n" % (row_actions[i], dnp[wp.game.players[0]][i],
                                                               col_actions[i], dnp[wp.game.players[1]][i]))

    # denormalized games
    for wp in sorted_profiles:
        name = wp.game.title[wp.game.title.rindex('.')+1:].replace("_", "-")[len("cn_"):]
        fname = name + ".nfg"
        g = gambit.Game.new_table([n_row,n_col])
        for i in xrange(n_row):
            for j in xrange(n_col):
                g[i,j][0] = int(float(wp.game[i,j][0])/norm)
                g[i,j][1] = int(float(wp.game[i,j][1])/norm)
        with open(fname, 'wt') as out:
            out.write(repr(g))
    
        

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
