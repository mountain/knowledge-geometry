import numpy as np
import sh

from sh import gnuplot

script = '''#
# The quartic functions

set output '%s.png'

set terminal pngcairo transparent enhanced font "sans,10" fontscale 1.0 size 600, 400 
set key at screen 1, 0.9 right top vertical Right noreverse enhanced autotitle nobox
unset key

set style textbox  opaque margins  0.5,  0.5 fc  bgnd noborder linewidth  1.0
set view 20, 340, 1, 1.1
set isosamples 60, 60
set cntrlabel  format '%%8.3g' font ',7' start 2 interval 20
set hidden3d back offset 1 trianglepattern 3 undefined 1 altdiagonal bentover
set cntrparam order 8
set style data lines
set xyplane relative 0
set ztics  norangelimit logscale autofreq 
set xlabel "x" 
set xrange [ * : * ] noreverse writeback
set x2range [ * : * ] noreverse writeback
set ylabel "y" 
set yrange [ * : * ] noreverse writeback
set y2range [ * : * ] noreverse writeback
set zlabel "z" 
set zlabel offset character 1, 0, 0 font "" textcolor lt -1 norotate
set zrange [ * : * ] noreverse writeback
set cbrange [ * : * ] noreverse writeback
set rrange [ * : * ] noreverse writeback

quartic(x,y) = %s %0.5f*x*x*x*x %s %0.5f*x*x*x*y %s %0.5f*x*x*y*y %s %0.5f*x*y*y*y %s %0.5f*y*y*y*y

set contour
unset surface
unset ztics
unset zlabel
set cntrparam levels auto 20

set title "quartic function"
splot [-1.0:1.0] [-1.0:1.0] quartic(x,y)
'''

for ix in range(20):
    coeffs = 2 * np.random.random([5]) - 1
    c1, c2, c3, c4, c5 = coeffs

    s1 = '+' if c1 >= 0 else '-'
    s2 = '+' if c2 >= 0 else '-'
    s3 = '+' if c3 >= 0 else '-'
    s4 = '+' if c4 >= 0 else '-'
    s5 = '+' if c5 >= 0 else '-'
    c1 = - c1 if s1 == '-' else c1
    c2 = - c2 if s2 == '-' else c2
    c3 = - c3 if s3 == '-' else c3
    c4 = - c4 if s4 == '-' else c4
    c5 = - c5 if s5 == '-' else c5

    fname = 'quartic_%02d' % ix
    with open('%s.plot' % fname, 'w') as f:
        f.write(script % (fname, s1, c1, s2, c2, s3, c3, s4, c4, s5, c5))
        f.flush()

    gnuplot('-c', '%s.plot' % fname)