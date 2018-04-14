import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

prop = fm.FontProperties(fname='./font/braille.ttf')

plt.title('graph3.png', fontproperties=prop, size=32)
plt.xlabel('time in seconds', fontproperties=prop, size=32)
plt.ylabel('cell count', fontproperties=prop, size=32)
plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.savefig('graph3.png')

plt.show()