
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib
#pgf_with_rc_fonts = {"pgf.texsystem": "pdflatex"}
#matplotlib.rcParams.update(pgf_with_rc_fonts)


x = np.arange(-10, 10, 0.01)
alpha = 1.6733
l = 1.0507
y = l*((x > 0)*x + (x <= 0)*(alpha * np.exp(x) - alpha))

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

f = plt.figure()
ax = f.add_subplot(111)

ax.plot(x, y, color='b',linewidth=2)
ax.grid(b=True, which='major', color='r', linestyle='--')
plt.title('SELU(x) with \\lambda = {}, \\alpha = {}'.format(l, alpha))
ax.set_xticks(np.arange(-10, 11, 2))
plt.savefig('selu.png', dpi=200)

plt.show()
