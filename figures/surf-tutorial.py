import numpy as np
import mahotas as mh
from mahotas.features import surf
from scipy.cluster import vq
import mahotas.demos
impath = mh.demos.image_path('luispedro.jpg')
f = mh.imread(impath, as_grey=True)
f = f.astype(np.uint8)
spoints = surf.surf(f, 4, 6, 2)
descrs = spoints[:,6:]
_,cids = vq.kmeans2(vq.whiten(descrs), 5)
colors = np.array([
    [ 255,  25,   1],
    [203,  77,  37],
    [151, 129,  56],
    [ 99, 181,  52],
    [ 47, 233,   5]])
f2 = surf.show_surf(f, spoints[:64], cids, colors)
from matplotlib import pyplot as plt
plt.subplot(1,2,1)
plt.imshow(np.dstack([f,f,f]))
plt.xticks([])
plt.yticks([])
plt.subplot(1,2,2)
plt.imshow(f2)
plt.xticks([])
plt.yticks([])
plt.savefig('surf-tutorial.png')
