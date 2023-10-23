from train import train
from DumpAI import DumpAI
from Qlearning import QlearningAIOneLevel
from DQN import DQN_agent
from human import Human

NumPlayer = 2
LearningRate = 0.1
DiscountFactor = 0.5
Greedy_Epsilon = 0
Epoch = 1000000000

# trainDQN(DQN_agent, NumPlayer, True, LearningRate, DiscountFactor, Greedy_Epsilon, Epoch, Human, True)
train(QlearningAIOneLevel, NumPlayer, False, LearningRate, DiscountFactor,
      Greedy_Epsilon, Epoch, QlearningAIOneLevel, False, False)
