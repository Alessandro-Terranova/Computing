import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline
import scipy.integrate

class ProbabilityDensityFunction(InterpolatedUnivariateSpline):
    def __init__(self, x, y, degree):

        #normalizzo con simpson 
        Norm = scipy.integrate.simps(y, x, dx=1/len(x), even='first')
        y /= Norm
        #creo la spline dal costruttore della classe madre
        super().__init__(x, y, k=degree)

        #creo cdf(per punti)
        Y = np.array([self.integral(x[0], i) for i in x])
        #interpolo
        self.cf = InterpolatedUnivariateSpline(x, Y, k=degree)

        xq, iq = np.unique(Y, return_index=True) #np.unique seleziona i valori di Y diversi tra loro come xq indicizzandoli come i1

        yq = x[iq] #chiamo y1 gli x valutati negli indici non ripetuti

        #creo spline ppf (quantile)
        self.ppf = InterpolatedUnivariateSpline(xq, yq, k=degree) #ho già invertito x con y

    def prob(self, x1, x2):
        return self.cf(x2) - self.cf(x1)

    def rand(self, length):
        return self.ppf(np.random.uniform(size=length))

def test_triangular():
    """
    funzione di test su distribuzione triangolare
    """

    x = np.linspace(0, 1, 10000)
    y = np.zeros(len(x))

    #creo la distribuzione triangolare

    y[x<0.5] = x[x<0.5]
    y[x>0.5] = 1 - x[x>0.5]

    pdf = ProbabilityDensityFunction(x, y, 3)
    tri = pdf.rand(len(x))

    plt.figure(1)
    plt.plot(x, y, 'k')
    plt.hist(tri, bins=int(np.sqrt(len(x)-1)), density=True) #density=True normalizza la probabilità

def test_gaussian():
    """
    funzione di test su distribuzinoe gaussiana
    """

    x = np.linspace(-5, 5, int(1e4))
    y = np.exp(-x**2 / 2)

    #creo distribuzione gaussiana

    pdf = ProbabilityDensityFunction(x, y, 3)
    gauss = pdf.rand(len(x))

    plt.figure(2)
    plt.plot(x, y, 'k')
    plt.hist(gauss, bins=int(np.sqrt(len(x)-1)), density=True) #density=True normalizza la probabilità

if __name__ == '__main__':
    test_triangular()
    test_gaussian()
    plt.show()
