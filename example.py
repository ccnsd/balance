import balance as blc
import random
import matplotlib.pyplot as plt
nblc = blc.TriangularBalance(25,-1,0.3,0)
# print(nblc.Energy)
nblc.TriadDynamics(3)
print(nblc.TimeLine)
plt.plot(nblc.TimeLine[:,1], nblc.TimeLine[:,0],'.')
plt.show()
# print(nblc.Network.mean())

