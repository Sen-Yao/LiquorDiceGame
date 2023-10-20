from GameAI import train
from DumpAI import DumpAI
from Qlearning import QlearningAIOneLevel
from human import Human

NumPlayer = 2
LearningRate = 0.5
DiscountFactor = 0.5
Greedy_Epsilon = 0.2
Epoch = 100000000

# train(QlearningAIOneLevel, NumPlayer, False, LearningRate, DiscountFactor, Greedy_Epsilon, Epoch, Human, True)
train(QlearningAIOneLevel, NumPlayer, True, LearningRate, DiscountFactor, Greedy_Epsilon, Epoch, QlearningAIOneLevel)
