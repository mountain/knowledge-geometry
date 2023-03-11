import numpy as np
import torch as th
import leibniz as lbnz
import pyvista as pv
import xarray as xr

from leibniz.core3d.gridsys.regular3 import RegularGrid
from leibniz.core3d.vec3 import mult, div, add, normalize, norm

wind = xr.open_dataset('prog/wind/wind.nc')

sphere = pv.Sphere(
    direction=(0, 0, 1),
    start_theta=0, end_theta=360, theta_resolution=1440,
    start_phi=0.001, end_phi=179.999, phi_resolution=721,
    radius=6371000.0)


def cast(data):
    d = data.reshape(721, 1440)
    return lbnz.cast(np.concatenate((d[:, 1439:1407:-1], d, d[:, 0:32:1]), axis=1)).reshape(1, 1, 721, 1504, 1)


def strip(data):
    d = data.reshape(1, 1, 721, 1504, 2)
    return d[:, :, :, 32:1472, 0:1]


def plot_scalar(varname, scl):
    f = scl[0, 0, :, :, 0].numpy()[::-1, ::-1].T.reshape(721 * 1440, 1)
    sphere[varname] = f
    sphere.set_active_scalars(varname)
    sphere.plot(cpos='xz', cmap='plasma')


def plot_vector(varname, vec):
    a, b, c = vec
    a, b, c = a[0, 0, :, :, 0].numpy(), b[0, 0, :, :, 0].numpy(), c[0, 0, :, :, 0].numpy()
    vectors = np.concatenate(
        (
            a[::-1, ::-1].T.reshape(721 * 1440, 1),
            b[::-1, ::-1].T.reshape(721 * 1440, 1),
            c[::-1, ::-1].T.reshape(721 * 1440, 1),
        ), axis=-1
    )
    sphere[varname] = vectors
    sphere.set_active_vectors(varname)
    plt = pv.Plotter()
    plt.add_mesh(sphere.arrows, lighting=False, scalar_bar_args={'title': "x"})
    plt.add_mesh(sphere, color="grey", ambient=0.6, opacity=0.5, show_edges=False)
    plt.show()


lbnz.default_device = -1

# setup grid system
lbnz.bind(RegularGrid(
    basis='lng,lat,alt',
    W=1504, L=721, H=2,
    east=0 - 0.25 * 32, west=360 + 0.25 * 32,
    north=-89.999, south=89.999,
    upper=11.0, lower=10.0
))
lbnz.use('x,y,z')
lbnz.use('xyz')
lbnz.use('theta,phi,r')
lbnz.use('thetaphir')

# u10 = cast(wind['u10'].data)
# v10 = cast(wind['v10'].data)
# u10 = th.cat((u10, u10), dim=4)
# v10 = th.cat((v10, v10), dim=4)
# wnd = (u10, v10, lbnz.zero)
# plot_scalar('wind velocity', strip(norm(wnd)))

# vortex = lbnz.curl(wnd)
# plot_scalar('length', strip(th.log(norm(vortex))))

plot_scalar('theta', strip(lbnz.theta))
plot_scalar('phi', strip(lbnz.phi))
plot_scalar('Theta', strip(norm(lbnz.thetaphir.theta)))
plot_scalar('Phi', strip(norm(lbnz.thetaphir.phi)))

u = mult(lbnz.thetaphir.theta, (np.sin(lbnz.phi), np.sin(lbnz.phi), np.sin(lbnz.phi)))
plot_scalar('u', strip(norm(u)))
plot_scalar('curl u', strip(norm(lbnz.curl(u))))

alpha_p = np.pi / 4
alpha_q = np.pi / 2

a = np.cos(alpha_p) * np.cos(lbnz.phi) + np.sin(alpha_p) * (np.sin(lbnz.theta) * lbnz.zero - np.cos(lbnz.theta) * np.sin(lbnz.phi))
b = np.cos(alpha_p) * lbnz.zero        + np.sin(alpha_p) * (np.sin(lbnz.theta) * lbnz.one  + np.cos(lbnz.theta) * lbnz.zero       )
p = add(mult(lbnz.thetaphir.theta, (a, a, a)), mult(lbnz.thetaphir.phi, (b, b, b)))

a = np.cos(alpha_q) * np.cos(lbnz.phi) + np.sin(alpha_q) * np.sin(lbnz.phi) * np.cos(lbnz.theta)
b = np.sin(alpha_q) * np.sin(lbnz.theta)
q = add(mult(lbnz.thetaphir.theta, (a, a, a)), mult(lbnz.thetaphir.phi, (b, b, b)))

plot_scalar('p', strip(norm(p)))
plot_scalar('q', strip(norm(q)))

vp = lbnz.curl(p)
vq = lbnz.curl(q)

plot_scalar('vp', strip(norm(vp)))
plot_scalar('vq', strip(norm(vq)))

print(th.sum(lbnz.dot(vp, vp) * lbnz.dV))
print(th.sum(lbnz.dot(vq, vq) * lbnz.dV))
print(th.sum(lbnz.dot(vp, vq) * lbnz.dV))

