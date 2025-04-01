import random
from vector import vector   #   For Direction
from Constants import *

#   Each dot has a brain that stores all the forces that are applied on it.
class Brain:
    #   Brain.stepCount stores the max total number of steps current generation will take
    stepCount = INITIAL_STEP_COUNT
    def __init__(self):
        self.steps = 0          #   stores how many steps the dot has taken at any moment
        self.directions = []    #   stores all the forces 

    def __init__(self, size):
        self.steps = 0
        self.directions = [vector(0,0) for i in range(size)]
        self.randomize()

    #   Makes all directions completely random
    def randomize(self):
        for i in range(len(self.directions)):
            self.directions[i] = vector.random_dir()

    #   Returns a copy of the brain
    def clone(self):
        Clone = Brain(Brain.stepCount)
        for i in range(Brain.stepCount):

            #   Old steps are retained. Newer steps are randomized
            if i < len(self.directions):
                Clone.directions[i] = self.directions[i].copy()
            else:
                Clone.directions[i] = vector.random_dir()

        return Clone

    #    mutates all the directions 
    def mutate(self):
        for i in range(len(self.directions)):
            rnd = random.random()       #   returns a float in the range [0,1]

            if rnd < RATE_OF_MUTATION:  #   This works because probability of a random number between 0 and 1 being less than the RATE is equal to the RATE
                self.directions[i] = vector.random_dir()

