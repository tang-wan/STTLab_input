#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 16})

#==============================================================================

def set_axes_equal(ax: plt.Axes):
    """Set 3D plot axes to equal scale.

    Make axes of 3D plot have equal scale so that spheres appear as
    spheres and cubes as cubes.  Required since `ax.axis('equal')`
    and `ax.set_aspect('equal')` don't work on 3D.
    """
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)
    ax.set_box_aspect([1,1,1])


def _set_axes_radius(ax, origin, radius):
    x, y, z = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    ax.set_zlim3d([z - radius, z + radius])


def create_sphere_mesh(ntheta, nphi):
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:60j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    return x, y, z

#==============================================================================

def plot_sphere_frame(ax, num=10, **kwargs):
    theta = np.linspace(0, 2*np.pi, 100)
    for angle in np.linspace(-np.pi, np.pi, num):
        xlat = np.cos(theta)*np.cos(angle)
        ylat = np.sin(theta)*np.cos(angle)
        zlat = np.ones_like(theta)*np.sin(angle)
        xlon = np.sin(angle)*np.sin(theta)
        ylon = np.cos(angle)*np.sin(theta)
        zlon = np.cos(theta)
        ax.plot(xlat, ylat, zlat, **kwargs)
        ax.plot(xlon, ylon, zlon, **kwargs)


def plot_sphere_surface(ax, ntheta=10, nphi=20, **kwargs):
    sphere_mesh = create_sphere_mesh(ntheta, nphi)
    ax.plot_surface(*sphere_mesh, **kwargs)


def plot_sphere_axis(ax):
    ax.plot([-1,1], [ 0,0], [ 0,0], color='gray')
    ax.plot([ 0,0], [-1,1], [ 0,0], color='gray')
    ax.plot([ 0,0], [ 0,0], [-1,1], color='gray')
    ax.text(1.1, 0, 0, 'x')
    ax.text(0, 1.1, 0, 'y')
    ax.text(0, 0, 1.1, 'z')

#==============================================================================

data = np.loadtxt('results_time.txt')
t = data[:,0]
#track_m1 = data[:,[1,2,3]]
track_m1 = data[:,[4,5,6]]

#--------------------------------------

fig = plt.figure(figsize=(5,3*2))

# plot M-t
ax2 = plt.subplot2grid((3,1), (2,0))
ax2.plot(t/1e-9, track_m1[:,0], label='Mx')
ax2.plot(t/1e-9, track_m1[:,1], label='My')
ax2.plot(t/1e-9, track_m1[:,2], label='Mz')
ax2.set_xlabel('Time ($10^{-9}$ sec)')
ax2.set_ylabel('M')
ax2.legend()

# plot 3D track
ax1 = plt.subplot2grid((3,1), (0,0), rowspan=2,  projection='3d')
plot_sphere_frame(ax1, num=10, color='black', alpha=0.05)
plot_sphere_surface(ax1, ntheta=30, nphi=60, color='#808080', alpha=0.05)
plot_sphere_axis(ax1)
ax1.plot(*track_m1.T, color='red')

# set figure appearance
fig.tight_layout()
ax1.view_init(elev=30, azim=30)
#ax1.view_init(elev=90+30, azim=180)
ax1.set_xbound(-0.6, 0.6)
ax1.set_ybound(-0.6, 0.6)
ax1.set_zbound(-0.6, 0.6)
ax1.set_axis_off()
set_axes_equal(ax1)

#--------------------------------------

fig.savefig('Figure.png')
#plt.show()
