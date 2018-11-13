import balance as blc
import random
nblc = blc.TriangularBalance(45,0.7,0,0)
print(nblc.Energy)
nblc.TriadDynamics(4)
print(nblc.Energy)
