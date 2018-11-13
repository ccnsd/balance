import numpy as np
import networkx as nx
import random

class TriangularBalance:
    def __init__(self, size, initialRatio, AgeExponent, noiseType):
        self.Size           = size
        self.TrianglesOnLink= self.LinkTriangles()
        self.Triangles      = self.TriangleCount()
        self.InitRatio      = initialRatio
        self.AgeExponent    = AgeExponent
        self.NoiseType      = noiseType
        self.NetworkInitiator()
    #region Initial Functions
    def TriangleCount(self):
        numinator   = (self.Size) * (self.Size - 1) * (self.Size - 2)
        denominator = 6
        return(numinator/denominator)
    
    def LinkTriangles(self):
        trianglesOnLink = self.Size - 2
        return(trianglesOnLink)

    # This function initializes the network at the begining of the run
    def NetworkInitiator(self):
        tempMatrix = np.random.rand(self.Size,self.Size)
        tempMatrix[tempMatrix < self.InitRatio]  = -1
        tempMatrix[tempMatrix >= self.InitRatio] = 1
        adjMatrix = np.tril(-tempMatrix, -1) + np.tril(-tempMatrix,-1).T      
        self.InitialNetwork = adjMatrix
        self.Network        = self.InitialNetwork
        self.Energy         = self.NetworkEnergy()
    
    # This functio calculates the total energy of the netwrok
    def NetworkEnergy(self):
        netLen2Path            = np.matmul(self.Network,self.Network)
        energyMat              = np.multiply(self.Network, netLen2Path)
        # Every link is counted 2 times
        unnormalTotalEnergy    = np.sum(energyMat) / 2
        # Every triangle is counted 3 times
        unnormalTotalEnergy    = unnormalTotalEnergy / 3
        # We want energy to be between -1 to +1
        totalEnergy            = float(-unnormalTotalEnergy) / self.Triangles
        return(totalEnergy)
    #endregion
    
    #region Dynamics
    # Calculation of the attribution of one link in the total energy of the network
    def LinkEnergy(self, adjTuple):
        linkSign = self.Network[adjTuple]
        linkRow  = self.Network[adjTuple[0]]
        linkCol  = self.Network[adjTuple[1]]
        linkEng  = float(-1.0 * np.inner(linkRow, linkCol) * linkSign) / self.Triangles
        return(linkEng)

    def TriadDynamics(self, itterateExp):
        itterateLength = self.Size ** itterateExp
        for i in range(itterateLength):
            link = tuple(random.sample(range(0,self.Size-1),2))
            linkSign = self.Network[link]
            linkEnergy = self.LinkEnergy(link)
            tempEnergy = linkEnergy + 1/(2 * self.Triangles) if random.random() < 0.5 else linkEnergy - 1/(2 * self.Triangles)
            tempSign = linkSign if tempEnergy < 0 else -linkSign
            delta = abs(tempSign - linkSign) * linkEnergy
            self.Energy -= delta
            self.Network[link] = tempSign
            self.Network[link[1]][link[0]] = tempSign
    #endregion



