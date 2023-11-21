import numpy as np
import math
from scipy import special
import matplotlib.pyplot as plt
import matplotlib as mpl

def radial_function(a0, n, l, r):
    """
    Calculate the normalized radial component of the wavefunction with reduced 
    mass and Laguerre polynomials. 

    https://faculty.washington.edu/seattle/physics227/reading/reading-26-27.pdf

    Input(s):
    a0: float, Bohr radius
    n: int, principal quantum number
    l: int, azimuthal quantum number
    r: numpy.array, radial coordinates

    Output(s)
    numpy.array: R(r) wavefunction radial component

    """
    C = np.sqrt((2 / (n * a0))**3 * math.factorial(n - l - 1) / 
                (2 * n * math.factorial(n + l)**3))
    
    Laguerre = special.genlaguerre(n - l - 1, 2 * l + 1)

    P = 2 * r / (n * a0)

    return C * np.exp(-P / 2) * P**l * Laguerre(P)

def angular_function(l, m, theta, phi):
    """
    Calculate the angular components of the wavefunction using Legendre polynomials. 

    https://faculty.washington.edu/seattle/physics227/reading/reading-26-27.pdf

    Input(s):
    l: int, azimuthal quantum number
    m: int, magnetic quantum number
    theta: numpy.array, polar angles
    phi: int, azimuthal angle, int for 2D

    Output(s)
    numpy.array: Y(theta, phi) wavefunction angular component

    """

    C = (-1)**m * np.sqrt((2 * l + 1) * math.factorial(l - m) / 
                          (4 * math.pi * math.factorial(l + m)))

    Legendre = special.lpmv(m,l,np.cos(theta))


    return C * Legendre * np.real(np.exp(1.j * m * phi))

def wave_function (a0_scale_factor, n, l, m, x, y):

    """
    Calculate the wave function radial and angular components. 

    Input(s):
    a0_scale_factor: float, scalar to make wavefunction view-able
    n: int, principal quantum number
    l: int, azimuthal quantum number
    m: int, magnetic quantum number
    r: numpy.array, radial coordinates 
    theta: numpy.array, polar angles
    phi: int, azimuthal angle, int for 2D

    Output(s)
    numpy.array: Wavefunction

    """

    r = np.sqrt(x**2 + y**2) # grid to radial coordinates

    eps = np.finfo(float).eps
    theta = np.arctan(x / (y + eps)) # grid to angular, eps for zero handling
    phi = 0

    a0 = a0_scale_factor * (5.29177210903e-11) * 1e+12

    R = radial_function(a0, n, l, r)
    Y = angular_function(l, m, theta, phi)

    psi = R * Y

    return psi

def probability_density(psi):
    """
    Calculate the probability density by taking the magnitude of the wavefunction.

    Input(s)
    psi: numpy.array, wavefunction

    Output(s):
     numpy.array, probability density function
    """
    return np.abs(psi)**2

def plot_radial_component():
    return

def plot_probability_density(n, l, m, a0_scale_factor):

    #plt.rcParams 

    fig, ax = plt.subplots(figsize=(16, 16))
    plt.subplots_adjust(top=0.80)
    plt.subplots_adjust(right=0.90)
    #plt.subplots_adjust(left=-0.1)

    # Compute and visualize the wavefunction probability density
    psi = wave_function(a0_scale_factor, n, l, m)
    prob_density = probability_density(psi)
    im = ax.imshow(np.sqrt(prob_density), cmap = mpl.colormaps['magma'])

    cbar = plt.colorbar(im)
    cbar.set_ticks([])

    #plt.style.use('style_name')
    plt.rcParams['text.color'] = '#000000'
    plt.rcParams["font.family"] = "sans-serif"
    ax.tick_params(axis='x', colors='#ffffff')
    ax.tick_params(axis='y', colors='#ffffff')

    #ax.set_title('Hydrogen Atom - Wavefunction Electron Density', fontsize=24, loc='left', color='#000000')
    """ax.text(5, 40, (
        r'$|\psi_{n \ell m}(r, \theta, \varphi)|^{2} ='
        r' |R_{n\ell}(r) Y_{\ell}^{m}(\theta, \varphi)|^2$'
    ), fontsize=20, color='#ffffff')"""
   
    ax.text(5, 80, r'n, l, m = $({0}, {1}, {2})$'.format(n, l, m), color='#dfdfdf', fontsize=20) 
    ax.text(1125,775, 'Electron probability distribution', rotation=-90, fontsize=24)
    ax.text(1125, 40, 'Higher\nprobability', fontsize=12,)
    ax.text(1125, 990, 'Lower\nprobability', fontsize=12)
    #ax.invert_yaxis()

def plot2(a0, n, l, r):

    R_nl = radial_function(a0, n, l, r)
    P_r = 4 * math.pi * r**2 * R_nl**2
    print((R_nl.shape))

    plt.plot(r/a0,P_r)
    fig, ax = plt.subplots()
    return fig

x = np.linspace(-500,500,1000)
y = np.linspace(-500,500,1000)
x,y = np.meshgrid(x,y)
r = np.sqrt(x**2 + y**2)

a0 = (5.29177210903e-11) * 1e+11
n = 3
l = 0
m = 0


fig = plot2(a0, n, l, r)

plt.show()


        