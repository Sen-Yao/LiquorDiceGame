from ClassicAI import ClassicAI
# from Qlearning import QlearningAIOneLevel
from train import train
from DQN import DQN_agent
from Play import play
from random_train import RandomTrain

NumPlayer = 2
LearningRate = 0.001
DiscountFactor = 0.5
Greedy_Epsilon = 0
Epoch = 1000000000

# play(DQN_agent, 2, False)

# RandomTrain(DQN_agent, DQN_agent, 0.001, 0.1, 4000, 2, False)

# train(DQN_agent, ClassicAI, 0.0001, 0.3, 1000000, 2, False)

play(DQN_agent, 2, True, True, False)
