from train import train, trainDQN
from DumpAI import DumpAI
from Qlearning import QlearningAIOneLevel
from DQN import DQN_agent
from human import Human

NumPlayer = 2
LearningRate = 0.3
DiscountFactor = 0.5
Greedy_Epsilon = 0.2
Epoch = 1000000000

# trainDQN(QlearningAIOneLevel, NumPlayer, False, LearningRate, DiscountFactor, Greedy_Epsilon, Epoch, Human, True)
# trainDQN(QlearningAIOneLevel, NumPlayer, True, LearningRate, DiscountFactor, Greedy_Epsilon, Epoch, QlearningAIOneLevel)
trainDQN(DQN_agent, NumPlayer, True, LearningRate, DiscountFactor, Greedy_Epsilon, Epoch, QlearningAIOneLevel)
