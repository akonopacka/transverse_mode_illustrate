import numpy as np
import math
from scipy.special import jv,kn
from matplotlib import pyplot as plt

def pyfindpeaks( environment, valuelist , thresh):
    """Determine peak positions in a list or array of real values.
    Arguments:
      - environment: (INT) a maxima has to be the local maximum in this environment of points
      - valuelist: list or array of points to find the maxima in
      - thresh: a maximum has to be larger than this value
    Returns:
      - listindices: positions of the peaks found
    """
    def limitss(diff,length,pos):
    #this prevents hitting the borders of the array
        mi = np.max( [0, pos-diff])
        ma = np.min( [length, pos+diff])
        return mi,ma
    #range left/right
    half = int( np.floor( environment/2))
    valuelistlength = len(valuelist)
    #pre-filter the peaks above threshold
    abovethresh = np.nonzero( valuelist>thresh )[0]
    i = 0
    peakpos =np.array([],int)
    # circle through the candidates
    while (i < len(abovethresh)):
        mi,ma = limitss(half, valuelistlength, abovethresh[i])
        partialvaluelist = valuelist[mi:ma]
    # is the valuelist value of the actual position the maximum of the environment?
        if valuelist[abovethresh[i]] == max(partialvaluelist):
            peakpos=np.append(peakpos,abovethresh[i])
        i = i+1
    return peakpos


def jkdiff(m,u,w):
    """Calculate the absolute difference diff = |Jm(u)/Jm+1(u)-Km(w)/Km+1(w)|.
    Can be used to determine the branches of LP modes in a step-index fiber.
    Arguments:
        - m azimuthal number of periods (m=0,1,2,3...)
        - u radial phase constant
        - w radial decay constant
    Returns:
        - diff - Difference
    """
    return np.abs(  jv(m, u)/(u * jv(m+1,u)) - (kn(m,w)/(w*kn(m+1,w))))

def calc_jkdiff_matrix(m, Vmax, pts=300):
    """ calculate the Difference
        diff = |Jm(u)/Jm+1(u)-Km(w)/Km+1(w)|
        for a given m for a matrix
        [0..Vmax] x [0..Vmax] with pts x pts values.
    Arguments:
        - m: azimuthal number of periods (m=0,1,2,3...)
        - Vmax:  maximum V-number, normalized frequency
    Optional Arguments:
        - pts: number of grid points for each of the two
               axes of the matrix
    Returns:
        - jkdiffmatrix
        - uv : u vector (=w vector)
    """
    uv = np.linspace(0, Vmax, pts)
    uu, ww = np.meshgrid(uv, uv)
    uu2 = np.reshape(uu, pts * pts)
    ww2 = np.reshape(ww, pts * pts)
    diff = jkdiff(m, uu2, ww2)
    diff = np.reshape(diff, [pts, pts])
    return diff, uv

def get_intersects(m, V, anglepts=500, peakfindpts=5, maxjkdiff=1e-2):
    """Calculate the intersects of the V-circle with the branches of LPmp for given m
    Arguments:
        - m azimuthal number of periods (m=0,1,2,3...)
        - V  maximum V-number, normalized frequency
    Optional arguments:
        - anglepts: number of points for the circle (default=500)
        - peakfindpts: intersection points are determined by searching
                       for peaks of 1/jkdiff along the V-circle.
                       For an u-w pair to be recognized as peak,
                       it must be a maximum in a surrounding of
                       peakfindpts points.
        - maxjkdiff: sets the maximum value for jkdiff, so that
                     an intersection is still recognized
    Returns:
        - reslist: list of branch intersections found.
            consists of sub-lists [u, w, modename]
    """
    epsi = 1e-5

    angle = np.linspace(np.pi/2.0-epsi, epsi, anglepts)
    w = np.sin(angle) * V
    u = np.cos(angle) * V
    pl = pyfindpeaks(peakfindpts, 1./jkdiff(m, u, w), 1./maxjkdiff)
    res = []
    for ii,p in enumerate(pl):
        res.append([u[p], w[p],"LP%d%d"%(m,ii+1)])
    return res


def besselmode(m, u, w, x, y, phioff=0):
    """Calculate the field of a bessel mode LP mode.
    Arguments:
        - m azimuthal number of periods (m=0,1,2,3...)
        - u, w  radial phase constant and radial decay constant
        - x, y transverse coordinates
        - phioff: offset angle, allows to rotate the mode in
                  the x-y plane
    Returns:
        - mode: calculated bessel mode
    """
    xx,yy = np.meshgrid(x,y)
    rr = np.reshape( np.sqrt(xx**2 + yy**2), len(x)*len(y))
    phi = np.reshape( np.arctan2(xx,yy), len(x)*len(y))
    fak = jv(m,u)/kn(m, w)
    res = np.zeros(len(rr))
    indx1 = rr<=1
    res[indx1] = jv(m,u*rr[indx1])*np.cos(m*phi[indx1]+phioff)
    indx2 = rr>1
    res[indx2] = fak * kn(m, w * rr[indx2]) * np.cos(m * phi[indx2] + phioff)
    res = res / np.max(np.abs(res))
    return np.reshape(res, [len(y), len(x)])


def calculate_v(lambda_, a, NA):
    v = (2 * math.pi * (a/2) * NA) / lambda_
    print("Value of V-number :", v)
    return v


def get_chart(lambda_, a, NA):
    V = calculate_v(lambda_, a, NA)

    # # set the V-number
    # V=4.5

    # look for LP modes up to LP_mmax,x
    mmax = 1  

    # for m in range(mmax+1):
    #     intersects = get_intersects(m, V)
    #     print("\nm=%d, # of intersections: %d\n"%(m, len(intersects)))
    #     for intersect in intersects:
    #         print("  %s u=%.3f w=%.3f"%(intersect[2], intersect[0], intersect[1]))

        # x-and y vector for the modes to be calculated
    x = np.linspace(-2,2,500)   # in units of a
    y = x 

    # LP01 mode
    m=1
    intersects = get_intersects(m, V)
    intersect = intersects[0]
    # u=1.958
    # w=4.052
    u = intersect[0]
    w = intersect[1]
    print("  %s u=%.3f w=%.3f"%(intersect[2], u, w))

    m01 = besselmode(m, u, w, x, y)
    figure = plt.figure()
    plt.imshow(m01, extent=(min(x), max(x), min(y), max(y)), clim=[-1,1], cmap='bwr')
    plt.colorbar()

    return figure
