import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# prop = fm.FontProperties(fname='./font/braille.ttf')

# fig = plt
# fig.title('graph3.png', fontproperties=prop, size=32)
# fig.xlabel('time in seconds', fontproperties=prop, size=32)
# fig.ylabel('cell count', fontproperties=prop, size=32)
# fig.plot([1, 2, 3, 4], [1, 4, 9, 16], linewidth=3.0)

# # fig.set_size_inches(6, 8)
# fig.savefig('graph3.png', dpi=72)
# # plt.savefig("test.png")

# fig.show()


plt.title('graph3.png', size=32)
plt.xlabel('time (s)', size=32)
plt.ylabel('cell count', size=32)
plt.plot([1,2,3,4],[1,4,9,16], linewidth=4.0)
plt.savefig('graph3.png', dpi=20)