from pylab import *
import numpy as np

dx = 0.0001
e = 2.718281828

def fu(x):
    return np.sqrt(np.log(x))
    return (x**2)*(np.exp(x))

def der(a):
    return (fu(a+dx)-fu(a))/dx

x_verdier = linspace(-5, 5, 1000)
y_verdier = fu(x_verdier)
dy_verdier = der(x_verdier)

plot(x_verdier, y_verdier, label='f(x)')
plot(x_verdier, dy_verdier, label="f'(x)")
ylim(-5, 5)

axhline(0, color='black')
axvline(0, color='black')

legend()
show()

print("info:")

print(fu(1))
print(der(3))

v2_1=fu(3-dx)
v2_2=fu(3+dx)
v2_d=(v2_2-v2_1)/2
print(v2_d/dx)


