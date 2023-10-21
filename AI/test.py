from train import trainDQN
from DumpAI import DumpAI
from Qlearning import QlearningAIOneLevel
from DQN import DQN_agent
from human import Human

NumPlayer = 2
LearningRate = 0.5
DiscountFactor = 0.5
Greedy_Epsilon = 0.1
Epoch = 1000000000

# trainDQN(QlearningAIOneLevel, NumPlayer, False, LearningRate, DiscountFactor, Greedy_Epsilon, Epoch, Human, True)
trainDQN(QlearningAIOneLevel, NumPlayer, False, LearningRate, DiscountFactor, Greedy_Epsilon, Epoch, QlearningAIOneLevel)
