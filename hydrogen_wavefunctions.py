import numpy as np
import math
from scipy import special
import matplotlib.pyplot as plt

def radial_function(a0, n, l, r):
    """
    Compute the normalized radial component of the wavefunction with reduced 
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
    Compute the angular components of the wavefunction using Legendre polynomials. 

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

def wave_function (a0_scale_factor, n, l, m, r, theta, phi):

    a0 = a0_scale_factor * (5.29177210903e-11) * 1e+12

    R = radial_function(a0, n, l, r)
    Y = angular_function(l, m, theta, phi)

    psi = R * Y

    return psi

x = y = np.linspace(-500,500,1000)
x, y = np.meshgrid(x,y)

r = np.sqrt(x**2 + y**2) # grid to radial coordinates

eps = np.finfo(float).eps
theta = np.arctan(x / (y + eps)) # grid to angular, eps for zero handling
phi = 0

n = 2 # Principal quantum number
l = 1 # Azimuthal quantum number, n-1
m = 1 # Magnetic quantum number, 
#a0_scale_factor = 1 * 10**12


def probability_density(psi):
    return np.abs(psi)**2

def plot_radial_component():
    return

def plot_probability_density(n, l, m, a0_scale_factor):

    fig, ax = plt.subplots(figsize=(16, 16.5))
    plt.subplots_adjust(top=0.82)
    plt.subplots_adjust(right=0.905)
    plt.subplots_adjust(left=-0.1)

    # Compute and visualize the wavefunction probability density
    psi = wave_function(a0_scale_factor, n, l, m, r, theta, phi)
    prob_density = probability_density(psi)
    im = ax.imshow(np.sqrt(prob_density))

    cbar = plt.colorbar(im, fraction=0.046, pad=0.03)
    cbar.set_ticks([])

    theme = 'lt'
    plt.rcParams['text.color'] = '#000000'
    title_color = '#000000'
    ax.tick_params(axis='x', colors='#000000')
    ax.tick_params(axis='y', colors='#000000')

    ax.set_title('Hydrogen Atom - Wavefunction Electron Density', pad=130, fontsize=44, loc='left', color=title_color)
    ax.text(0, 722, (
        r'$|\psi_{n \ell m}(r, \theta, \varphi)|^{2} ='
        r' |R_{n\ell}(r) Y_{\ell}^{m}(\theta, \varphi)|^2$'
    ), fontsize=36)
    ax.text(30, 615, r'$({0}, {1}, {2})$'.format(n, l, m), color='#dfdfdf', fontsize=42)
    ax.text(770, 140, 'Electron probability distribution', rotation='vertical', fontsize=40)
    ax.text(705, 700, 'Higher\nprobability', fontsize=24)
    ax.text(705, -60, 'Lower\nprobability', fontsize=24)
    ax.text(775, 590, '+', fontsize=34)
    ax.text(769, 82, '−', fontsize=34, rotation='vertical')
    ax.invert_yaxis()

    plt.show()

plot_probability_density(3,1,1,0.6)

