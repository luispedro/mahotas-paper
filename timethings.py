import numpy as np
import timeit
import mahotas
luispedro_image = 'mahotas/demos/data/luispedro.jpg'
f = mahotas.imread(luispedro_image, as_grey=True)
markers = np.zeros_like(f)
markers[100,100] = 1
markers[200,200] = 2
f = f.astype(int)
markers = markers.astype(int)
otsu = mahotas.otsu(f.astype(np.uint8))
fbin = f > otsu
Bc = np.eye(3)
Bc = Bc.astype(bool)

pre ='''
import numpy as np
import mahotas
import pymorph
import timethings
fbin = timethings.fbin
f = timethings.f
Bc = timethings.Bc
markers = timethings.markers
'''

def t(s):
    return timeit.timeit(s, setup=pre, number=24)
if __name__ == '__main__':
    base = t('np.max(f)')
    for name,statement, alt in [
                ('erode', 'mahotas.erode(fbin, Bc)', 'pymorph.erode(fbin, Bc)'),
                ('dilate', 'mahotas.dilate(fbin, Bc)', 'pymorph.dilate(fbin, Bc)'),
                ('open', 'mahotas.open(fbin, Bc)', 'pymorph.open(fbin, Bc)'),
                ('center mass', 'mahotas.center_of_mass(f)', None),
                ('cwatershed', 'mahotas.cwatershed(f, markers)', 'pymorph.cwatershed(f, markers)'),
                ('daubechies', 'mahotas.daubechies(f, "D4")', None),
                ('haralick', 'mahotas.features.haralick(f)', None),
                ]:
        time = '%.2f' % (t(statement)/base)
        alttime = 'NA'
        if alt is not None:
            alttime = '%.2f' % (t(alt)/base)
        print r"%-12s& %8s & %8s \\" % (name, time, alttime)

