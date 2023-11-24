import numpy as np
import math
from scipy import special


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
    Y: numpy.array, Y(theta, phi) wavefunction angular component

    """

    C = (-1)**m * np.sqrt((2 * l + 1) * math.factorial(l - m) / 
                          (4 * math.pi * math.factorial(l + m)))

    Legendre = special.lpmv(m,l,np.cos(theta))

    Y = C * Legendre * np.real(np.exp(1.j * m * phi))

    return Y

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
    R: numpy.array, R(r) wavefunction radial component

    """
    C = np.sqrt((2 / (n * a0))**3 * math.factorial(n - l - 1) / 
                (2 * n * math.factorial(n + l)**3))
    
    Laguerre = special.genlaguerre(n - l - 1, 2 * l + 1)

    P = 2 * r / (n * a0)

    R = C * np.exp(-P / 2) * P**l * Laguerre(P)

    return R

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
    psi: numpy.array: wavefunctions

    """

    r = np.sqrt(x**2 + y**2) # Grid to radial coordinates

    eps = np.finfo(float).eps
    theta = np.arctan(x / (y + eps)) # Grid to angular, eps for zero handling
    phi = 0

    a0 = a0_scale_factor # (5.29177210903e-11) * 1e+11

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
    P: numpy.array, probability density function
    """
    P = np.abs(psi)**2

    return P






        