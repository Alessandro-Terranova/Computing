import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

class ProbabilityDensityFunction:
    def __init__(self, x, y, degree):
        self.x = x
        self.y = y
        self.k = degree

        sp = InterpolatedUnivariateSpline(x, y, k=degree)
        Y =  np.array([sp.integral(x[0], i) for i in x])

        self.cf = InterpolatedUnivariateSpline(x, Y, k=self.k)

        xq, iq = np.unique(Y, return_index=True) #np.unique seleziona i valori di Y diversi tra lorro come xq indicizzandoli come i1

        yq = x[iq] #chiamo y1 gli x valutati negli indici non ripetuti

        self.ppf = InterpolatedUnivariateSpline(xq, yq, k=degree) #ho già invertito x con y

    def prob(self, x1, x2):
        return self.cf(x2) - self.cf(x1)

    def rand(self, length):
        return self.ppf(np.random.uniform(size=length))

if __name__ == '__main__':
    x = np.linspace(0, 1, 10000)
    y = np.zeros(len(x))
    
    #creo la distribuzione triangolare
    for i, t in enumerate(x):
        if t < 0.5:
            y[i] = 4*t
        else:
            y[i] = 4 - 4*t
    pdf = ProbabilityDensityFunction(x, y, 3)
    tri = pdf.rand(len(x))
    
    plt.figure(1)
    plt.plot(x, y, 'k')
    plt.hist(tri, bins=int(np.sqrt(len(x)-1)), density=True) #density=True normalizza la probabilità
    plt.show()
