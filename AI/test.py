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

# play(DQN_agent, 2, True)
# ergodic_train(DQN_agent, DumpAI, 0.0001, 0, 1, 8, True)
RandomTrain(DQN_agent, DQN_agent, LearningRate, Greedy_Epsilon, 10000000, 2, False)
