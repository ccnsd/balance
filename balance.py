import numpy as np
import networkx as nx

class TriangularBalance:
    def __init__(self, size, initialRatio, ageFactor, noiseType):
        self.Size           = size
        self.TrianglesOnLink= self.LinkTriangles()
        self.Triangles      = self.TriangleCount()
        self.InitRatio      = initialRatio
        self.AgeFactor      = ageFactor
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
        adjMatrix = np.random.rand(self.Size,self.Size)
        adjMatrix[adjMatrix < self.InitRatio]  = -1
        adjMatrix[adjMatrix >= self.InitRatio] = 1
        np.fill_diagonal(adjMatrix, 0)        
        self.InitialNetwork = -adjMatrix
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
        linkEng  = float(-1 * np.inner(linkRow, linkCol) * linkSign) / self.TrianglesOnLink
        return(linkEng)

    #endregion



