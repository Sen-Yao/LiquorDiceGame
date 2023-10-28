from train import train, ergodic_train
from DumpAI import DumpAI
from Qlearning import QlearningAIOneLevel
from DQN import DQN_agent
from human import Human
from Play import play
from random_train import RandomTrain

NumPlayer = 2
LearningRate = 0.001
DiscountFactor = 0.5
Greedy_Epsilon = 0
Epoch = 1000000000

# play(DQN_agent, 2, False)

RandomTrain(DQN_agent, DumpAI, LearningRate, 0.1, 200000, 2, False)

play(DQN_agent, 2, False)
