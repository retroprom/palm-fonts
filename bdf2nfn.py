#!/usr/bin/env python3

from argparse import ArgumentParser
from bdfparser import Font

ap = ArgumentParser('bdf2nfn')
ap.add_argument('i',type=str)
ap.add_argument('o',type=str)

def main():
        a = ap.parse_args()
        f = Font(a.i)
        h = f.headers
        p = f.props
        print(h)
        fbbx = h['fbbx']
        fbby = h['fbby']
        with open(a.o,'w') as n:
                n.write("// Generated by bdf2nfn from %s\n" % a.i)
                n.write("fontType 36864\n")
                n.write("fRecWidth %d\n" % fbbx)
                n.write("fRecHeight %d\n" % fbby)
                if 'font_ascent' in p:
                        n.write("ascent %d\n" % int(p['font_ascent']))
                if 'font_descent' in p:
                        n.write("descent %d\n" % int(p['font_descent']))
                for i in range(32,126):
                        c = chr(i)
                        g = f.glyph(c)
                        if not g:
                                print("warning: no '%s'" % c)
                        else:
                                if c.isprintable():
                                        n.write("GLYPH '%s'\n" % c)
                                else:
                                        n.write("GLYPH %d\n" % i)
                                b = [bin(int(h, 16))[2:].zfill(len(h) * 4) if h else '' for h in g.meta.get('hexdata')]
                                for l in b:
                                        s = str(l).replace('0','-').replace('1','#')[:g.meta['dwx0']]
                                        n.write(s + "\n")
                n.write("GLYPH -1\n")
                for y in range(fbby):
                        n.write('#'*fbbx+'\n')

if __name__ == '__main__':
        main()
