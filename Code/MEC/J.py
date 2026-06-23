from random import randint, randrange
import numpy as np
from Algos.Classes.Model import Model,Layers

# File contains Model J required by ED for inference tasks
def layer(a:int):

    oi = [(randrange(1,150)/1000) for _ in range(0,a)] #Output data size of each layer in MBs
    oi.sort()
    oi.reverse()
    np.array(oi)

    fi = [randrange(1000, 1000000) for _ in range (0,a)] #FLOPs
    fi.sort()
    fi.reverse()
    np.array(fi)

    return Layers(oi,fi)

mobilenet = Model(
    name="MobileNet",
    storage=50,
    layers= layer(27)
)

resnet18 = Model(
    name="Resnet18",
    storage=35,
    layers=layer(18)
)

resnet50 = Model(
    name="Resnet50",
    storage=120,
    layers=layer(50)
)

resnet34 = Model(
    name="Resnet34",
    storage=40,
    layers=layer(34)
)

vgg16 = Model(
    name="VGG16",
    storage=350,
    layers=layer(16)
)

vgg19 = Model(
    name="VGG19",
    storage=380,
    layers=layer(19)
)

inceptionv3 = Model(
    name="Inceptionv3",
    storage=120,
    layers= layer(23)
)

googlenet = Model(
    name="GoogleNet",
    storage=35,
    layers= layer(27)
)

alexnet = Model(
    name="AlexNet",
    storage=100,
    layers= layer(5)
)

densenet = Model(
    name="DenseNet",
    storage=150,
    layers=layer(121)
)

J = [googlenet,mobilenet,resnet18,resnet34,resnet50,alexnet,inceptionv3,vgg16,vgg19,densenet]