import skimage.morphology
import skimage.filter
import skimage.feature
import numpy as np
import timeit
import mahotas
import cv2

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
f = f.astype(np.uint8)
markers = markers.astype(int)
otsu = mahotas.otsu(f.astype(np.uint8))
fbin = f > otsu
fbin8 = fbin.astype(np.uint8)
Bc = np.eye(3)
Bc = Bc.astype(bool)
Bc8 = Bc.astype(np.uint8)
f3 = np.dstack([f,f,f])
f3 = f3.astype(np.uint8)
f3 = f3.copy()
filt = np.array([
    [1,0,-1,0],
    [2,2,3,-2],
    [-1,0,0,1]
    ])
markers32 = markers.astype(np.int32)

pre ='''
import skimage.filter
import skimage.morphology
import skimage.feature
import numpy as np
import mahotas
import pymorph
import cv2
import timethings
f = timethings.f
f3 = timethings.f3
fbin = timethings.fbin
fbin8 = timethings.fbin8
f64 = f.astype(np.float64)
Bc = timethings.Bc
Bc8 = timethings.Bc8
markers = timethings.markers
markers32 = timethings.markers32
filt = timethings.filt
'''

def t(s):
    return min(timeit.timeit(s, setup=pre, number=24) for i in xrange(3))

tests = [
    ('convolve', [
        'mahotas.convolve(f, filt)',
        None,
        None,
        None,
        ]),
    ('erode', [
        'mahotas.erode(fbin, Bc)',
        'pymorph.erode(fbin, Bc)',
        'skimage.morphology.erosion(fbin8, Bc8)',
        'cv2.erode(fbin8, Bc8)',
        ]),
    ('dilate', [
        'mahotas.dilate(fbin, Bc)',
        'pymorph.dilate(fbin, Bc)',
        'skimage.morphology.dilation(fbin8, Bc8)',
        'cv2.dilate(fbin8, Bc8)',
        ]),
    ('open', [
        'mahotas.open(fbin, Bc)',
        'pymorph.open(fbin, Bc)',
        'skimage.morphology.opening(fbin8, Bc8)',
        None,
        ]),
    ('center mass', [
        'mahotas.center_of_mass(f)',
        None,
        None,
        None,
        ]),
    ('sobel', [
        'mahotas.sobel(f, just_filter=True)',
        None,
        'skimage.filter.sobel(f)',
        'cv2.Sobel(f, cv2.CV_32F, 1, 1)',
        ]),
    ('cwatershed', [
        'mahotas.cwatershed(f, markers)',
        'pymorph.cwatershed(f, markers)',
        'skimage.morphology.watershed(f, markers)',
        'cv2.watershed(f3, markers32.copy())',
        ]),
    ('daubechies', [
        'mahotas.daubechies(f, "D4")',
        None,
        None,
        None,
        ]),
    ('haralick', [
        'mahotas.features.haralick(f)',
        None,
        'skimage.feature.greycoprops(skimage.feature.greycomatrix(f, [1], [0]))',
        None,
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
                time = '%.1f' % (t(st)/base)
                print '%8s &' % time,
        print r'\\'

