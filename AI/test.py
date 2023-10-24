from train import train, ergodic_train
from DumpAI import DumpAI
from Qlearning import QlearningAIOneLevel
from DQN import DQN_agent
from human import Human
from Play import play

NumPlayer = 2
LearningRate = 0.1
DiscountFactor = 0.5
Greedy_Epsilon = 0
Epoch = 1000000000

# play(DQN_agent, 2, True)
ergodic_train(DQN_agent, DumpAI, 0.001, 0, 10, 8, False)
