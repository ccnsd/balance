import balance as blc
import random
nblc = blc.TriangularBalance(21,0,0.3,0)
# print(nblc.Energy)
nblc.TriadDynamics(3)
print(nblc.Energy)
print(nblc.Network.mean())

