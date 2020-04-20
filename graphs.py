import numpy as np
import matplotlib.pylab as plt

x = np.linspace(-360, 360, 180)
#print(x)
rad = np.deg2rad(x)
plt.subplot(1,2,1)
plt.plot(x, np.sin(rad))
plt.title("Sine Wave")
plt.xlabel("Angle (degrees)")
xvals = range(-360, 361, 180)
plt.xticks(xvals)
plt.ylabel("Sin(x)")
plt.axis('tight')

plt.subplot(1,2,2)
plt.plot(x, np.cos(rad))
plt.title("Cosine Wave")
plt.xlabel("Angle (degrees)")
xvals = range(-360, 361, 180)
plt.xticks(xvals)
plt.ylabel("Cos(x)")
plt.axis('tight')
#plt.plot(x, np.sin(x) + np.cos(x))

plt.show()
