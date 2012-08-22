import numpy as np
import mahotas
from mahotas.features import surf
from os import path
from pylab import *
import milk

f = mahotas.imread('luispedro.jpg', as_grey=True)
f = f.astype(np.uint8)
spoints = surf.surf(f, 4, 6, 2)
descrs = spoints[:,6:]

values, _ = milk.kmeans(descrs, 5)
colors = np.array([(255-52*i,25+52*i,37**i % 101) for i in xrange(5)])

f2 = surf.show_surf(f, spoints[:64], values, colors)

subplot(1,2,1)
imshow(np.dstack([f,f,f]))
xticks([])
yticks([])
subplot(1,2,2)
imshow(f2)
xticks([])
yticks([])
savefig('surf-tutorial.png')
