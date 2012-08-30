import skimage.morphology
import skimage.filter
import skimage.feature
import numpy as np
import timeit
import mahotas

from os import path
luispedro_image = path.join(
            path.dirname(mahotas.__file__),
            'demos',
            'data',
            'luispedro.jpg')
f = mahotas.imread(luispedro_image, as_grey=True)
markers = np.zeros_like(f)
markers[100,100] = 1
markers[200,200] = 2
f = f.astype(int)
markers = markers.astype(int)
otsu = mahotas.otsu(f.astype(np.uint8))
fbin = f > otsu
fbin8 = fbin.astype(np.uint8)
Bc = np.eye(3)
Bc = Bc.astype(bool)
Bc8 = Bc.astype(np.uint8)

pre ='''
import skimage.filter
import skimage.morphology
import skimage.feature
import numpy as np
import mahotas
import pymorph
import timethings
f = timethings.f
fbin = timethings.fbin
fbin8 = timethings.fbin8
f64 = f.astype(np.float64)
Bc = timethings.Bc
Bc8 = timethings.Bc8
markers = timethings.markers
'''

def t(s):
    return timeit.timeit(s, setup=pre, number=24)

tests = [
    ('erode', [
        'mahotas.erode(fbin, Bc)',
        'pymorph.erode(fbin, Bc)',
        'skimage.morphology.opening(fbin8, Bc8)',
        ]),
    ('dilate', [
        'mahotas.dilate(fbin, Bc)',
        'pymorph.dilate(fbin, Bc)',
        'skimage.morphology.dilation(fbin8, Bc8)',
        ]),
    ('open', [
        'mahotas.open(fbin, Bc)',
        'pymorph.open(fbin, Bc)',
        'skimage.morphology.opening(fbin8, Bc8)',
        ]),
    ('center mass', [
        'mahotas.center_of_mass(f)',
        None,
        None,
        ]),
    ('sobel', [
        'mahotas.sobel(f)',
        None,
        'skimage.filter.sobel(f64)',
        ]),
    ('cwatershed', [
        'mahotas.cwatershed(f, markers)',
        'pymorph.cwatershed(f, markers)',
        'skimage.morphology.watershed(f, markers)',
        ]),
    ('daubechies', [
        'mahotas.daubechies(f, "D4")',
        None,
        None,
        ]),
    ('haralick', [
        'mahotas.features.haralick(f)',
        None,
        'skimage.feature.greycoprops(skimage.feature.greycomatrix(f, [1], [0]))',
        ]),
]
if __name__ == '__main__':
    base = t('np.max(f)')
    for name,statements in tests:
        print r'%-12s&' % name,
        for st in statements:
            if st is None:
                print '      NA &',
            else:
                time = '%.2f' % (t(st)/base)
                print '%8s &' % time,
        print r'\\'

