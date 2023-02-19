import numpy as np

# Spaten 
x1 = 4.20
s1 = 0.6646 
n1 = 322

# Heineken
x2 = 5.54
s2 = 1.105
n2 = 728

def graus_de_liberdade(s1, s2, n1, n2):
    a = s1**2 / n1
    b = s2**2 / n2

    num = (a + b) ** 2
    den = (a**2 / (n1+1)) + (b**2 / (n2+1))

    return num / den - 2

def estatistica_de_teste(x1, x2, s1, s2, n1, n2):
    a = s1**2 / n1
    b = s2**2 / n2
    return (x1 - x2) / np.sqrt(a + b)

def media_igual():

    v = graus_de_liberdade(s1, s2, n1, n2)
    print("v =", v)

    t0 = estatistica_de_teste(x1, x2, s1, s2, n1, n2)
    ta = 1.96245  # a = 5%

    print(f"|{t0}| > {ta}")
    print(abs(t0) > ta)


def variancia_igual():
    f0 = s1**2 / s2**2
    fa1 = 1.16572  # a = 1%
    fa2 = 0.82745   # a = 1%

    print(f"{f0} > {fa1} ou {f0} < {fa2}")
    print(f0 > fa1 or f0 < fa2)

media_igual()
print()
variancia_igual()