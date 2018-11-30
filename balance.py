import numpy as np
import networkx as nx
import random


class TriangularBalance:
    def __init__(self, size, initialRatio, AgeExponent, noiseType):
        # Size of the networ
        self.Size = size
        # Caclulate the number of triangles connected to one link
        self.TrianglesOnLink = self.LinkTriangles()
        # Calculate the number of all triangles in the fully connected network
        self.Triangles = self.TriangleCount()
        # The portion of friendly link
        self.InitRatio = initialRatio
        # The age factor
        self.AgeExponent = AgeExponent
        # The type of noise in memory
        self.NoiseType = noiseType
        # This will initialize the network based on given parameters
        self.NetworkInitiator()
    
    # region Initial Functions

    # Count all the triangles in network
    def TriangleCount(self):
        numinator = (self.Size) * (self.Size - 1) * (self.Size - 2)
        denominator = 6
        return(numinator/denominator)

    # Count the triangles connected to a link
    def LinkTriangles(self):
        trianglesOnLink = self.Size - 2
        return(trianglesOnLink)

    # This function initializes the network at the begining of the run
    def NetworkInitiator(self):
        # Generate a matrix with random elements between 0 and 1
        tempMatrix = np.random.rand(self.Size, self.Size)
        # Change elements smaller than friendship ratio to -1 (Will be changed to  1 soon)
        tempMatrix[tempMatrix < self.InitRatio] = -1
        # Change elements greater than friendship ratio to  1 (Will be changed to -1 soon)
        tempMatrix[tempMatrix >= self.InitRatio] = 1
        # The Created marix is not symmetric (and does not reperesnt a Graph) so we symmetrize it by this trick
        # Another point is that we change the sign of links here as we promised earlier
        adjMatrix = np.tril(-tempMatrix, -1) + np.tril(-tempMatrix, -1).T
        # Put this matrix to the class InitialNetwork and Network
        self.InitialNetwork = adjMatrix
        # To save the initial state we store the network in another variable
        self.Network = self.InitialNetwork
        # Birth matrix
        self.BirthTime = np.zeros((self.Size, self.Size))
        # Time of system
        self.SystemTime = 1
        # Calculate the Energy of our network
        self.Energy = self.NetworkEnergy()

    # This function calculates the total energy of the netwrok
    def NetworkEnergy(self):
        # Calculate the sum of product of all two pairs on each link
        netLen2Path = np.matmul(self.Network, self.Network)
        # Calculate the energy of all triangles on each link
        # (not exactly energy it needs a multiply by -1 to be energy)
        energyMat = np.multiply(self.Network, netLen2Path)
        # Every link is counted 2 times
        unnormalTotalEnergy = np.sum(energyMat) / 2
        # Every triangle is counted 3 times
        unnormalTotalEnergy = unnormalTotalEnergy / 3
        # We want energy to be between -1 to +1
        totalEnergy = float(-unnormalTotalEnergy) / self.Triangles
        return(totalEnergy)
    # endregion

    # region Dynamics
    # Calculation of the attribution of one link in the total energy of the network
    def LinkEnergy(self, adjTuple):
        # Get the link's sign
        linkSign = self.Network[adjTuple]
        # Adjacent links
        linkRow = self.Network[adjTuple[0]]
        linkCol = self.Network[adjTuple[1]]
        # The energy of triangles on the link
        linkEng = float(-1.0 * np.inner(linkRow, linkCol) * linkSign) / self.Triangles
        return(linkEng)

    def LinkEnergyCheck(self, linkEnergy, linkSign):
        # This part is for manipulating E=0 case
        randomSign = random.sample((1, -1), 1)
        addedEnergy = randomSign[0] / (2 * self.Triangles)
        tempEnergy = linkEnergy + addedEnergy
        # **************************************
        # link's new sign and energy change
        tempSign = - np.sign(tempEnergy) * linkSign
        delta = abs(tempSign - linkSign) * linkEnergy
        # *********************************
        return([delta, tempSign])

    def LinkBaseDynamics(self):
        # choose a random link
        link        = tuple(random.sample(range(0, self.Size-1), 2))
        # get the sign
        linkSign    = self.Network[link]
        # link energy
        linkEnergy  = self.LinkEnergy(link)
        # check if it will change
        engStat     = self.LinkEnergyCheck(linkEnergy, linkSign)
        # how much the sign should change
        signChange  = linkSign - engStat[1]
        # change system's energy and link's sign
        self.Energy                    -= engStat[0]
        self.Network[link]             -= signChange
        self.Network[link[1]][link[0]] -= signChange

    def BaseDynamics(self):
        # dynamics time length
        itterateLength = self.Size ** self.ItterateExp
        for _ in range(itterateLength):
            self.LinkBaseDynamics()

    def LinkAgeCheck(self, Age):
        # chack if link's age accepts the change
        agePass = int(random.random() < Age ** (self.AgeExponent - 1))
        return agePass

    def LinkAgedDynamics(self):
        # choose a random link
        link        = tuple(random.sample(range(0, self.Size-1), 2))
        # get the sign
        linkSign    = self.Network[link]
        # link energy
        linkEnergy  = self.LinkEnergy(link)
        # get the age of link
        linkAge     = self.SystemTime - self.BirthTime[link]
        # check if it will change due to energy
        engStat     = self.LinkEnergyCheck(linkEnergy, linkSign)
        # check if the age permits the change
        ageStat     = self.LinkAgeCheck(linkAge)
        # how much the enegy changes
        enrgChanged = engStat[0] * ageStat
        # how the sign changes
        signChange  = linkSign - engStat[1]
        # is the change happens?
        acceptStat  = signChange * ageStat
        # apply the changes
        self.Energy                     -= enrgChanged
        self.Network[link]              -= acceptStat
        self.Network[link[1]][link[0]]  -= acceptStat
        self.BirthTime[link]            += acceptStat * linkAge / 2
        self.BirthTime[link[1]][link[0]]+= acceptStat * linkAge / 2

    def AgedDynamics(self):
        print("Aged Dynamics")
        # dynamics time length
        itterateLength = self.Size ** self.ItterateExp
        for _ in range(itterateLength):
            self.LinkAgedDynamics()
            self.SystemTime += 1

    def TriadDynamics(self, itterateExp):
        self.ItterateExp = itterateExp
        # check if system has age or not
        aged = 0 < self.AgeExponent < 1
        self.AgedDynamics() if aged else self.BaseDynamics()
    # endregion
