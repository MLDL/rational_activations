![Logo](./images/rationals_logo_colored.png)
# Rational Activations - Learnable Rational Activation Functions
First introduce as PAU in Padé Activation Units: End-to-end Learning of Activation Functions in Deep Neural Network.

## 1. About Rational Activation Functions

Rational Activations are a novel learnable activation functions. Rationals encode activation functions as rational functions, trainable in an end-to-end fashion using backpropagation and can be seemingless integrated into any neural network in the same way as common activation functions (e.g. ReLU).

### Rationals: Beyond known Activation Functions
Rational can approximate any known activation function arbitrarily well (*cf. [Padé Activation Units: End-to-end Learning of Flexible Activation Functions in Deep Networks](https://arxiv.org/abs/1907.06732)*):
  ![rational_approx](./images/rational_approx.png)
  (*the dashed lines represent the rational approximation of every function)

Rational are made to be optimized by the gradient descent, and can discover good properties of activation functions after learning (*cf [Recurrent Rational Networks]()*):
  ![rational_properties](./images/rational_properties.png)
### Rationals evaluation on different tasks
* They were first applied (as Padé Activation Units) to supervized learning (image classification) in *[Padé Activation Units:...](https://arxiv.org/abs/1907.06732)*.

  ![sl_score](./images/sl_score.png)

  :octocat: See [rational_sl](https://github.com/ml-research/rational_sl) github repo

Rational matches or outperforms common activations in terms of predictive performance and training time.
And, therefore relieves the network designer of having to commit to a potentially underperforming choice.

* Recurrent Rational Functions have then been introduced in [Recurrent Rational Networks](), and both Rational and Recurrent Rational Networks are evaluated on RL Tasks.
  ![rl_scores](./images/rl_scores.png)
 :octocat: See [rational_rl](https://github.com/ml-research/rational_rl) github repo

## 2. Dependencies
    PyTorch>=1.4.0
    CUDA>=10.1


## 3. Installation

To install the rational_activations module, you can use pip, but:<br/>

:bangbang:  You should be careful about the CUDA version running on your machine.


To get your CUDA version:

    import torch
    torch.version.cuda

For **your** corresponding version of CUDA, please use one of the following command blocks:
#### CUDA 10.2

     pip3 install -U pip wheel
     pip3 install torch rational-activations

#### CUDA 10.1
##### Python3.6

       pip3 install -U pip wheel
       pip3 install torch==1.7.1+cu101
       pip3 install https://iron.aiml.informatik.tu-darmstadt.de/wheelhouse/cuda-10.1/rational_activations-0.0.19-cp36-cp36m-manylinux2014_x86_64.whl

##### Python3.7

       pip3 install -U pip wheel
       pip3 install torch==1.7.1+cu101
       pip3 install https://iron.aiml.informatik.tu-darmstadt.de/wheelhouse/cuda-10.1/rational_activations-0.0.19-cp37-cp37m-manylinux2014_x86_64.whl

##### Python3.8

         pip3 install -U pip wheel
         pip3 install torch==1.7.1+cu101
         pip3 install https://iron.aiml.informatik.tu-darmstadt.de/wheelhouse/cuda-10.1/rational_activations-0.0.19-cp38-cp38-manylinux2014_x86_64.whl


#### Other CUDA/Pytorch</h3>
For any other combinaison of python, please install from source:

     pip3 install airspeed
     git clone https://github.com/ml-research/rational_activations.git
     cd rational_activations
     python3 setup.py install --user



If you encounter any trouble installing rational, please contact [this person](quentin.delfosse@cs.tu-darmstadt.de).

## 4. Using Rational in Neural Networks

Rational can be integrated in the same way as any other common activation function.

~~~~
import torch
from rational_torch import Rational

model = torch.nn.Sequential(
    torch.nn.Linear(D_in, H),
    Rational(), # e.g. instead of torch.nn.ReLU()
    torch.nn.Linear(H, D_out),
)
~~~~

## 5. To be implemented
- [X] Make a documentation
- [X] Create tutorial in the doc
- [ ] Tensorflow working version
- [ ] Automatically find initial approx weights for function list
- [ ] Repair + enhance Automatic manylinux production script.
- [ ] Add python3.9 support
- [ ] Make an CUDA 11.0 compatible version
- [ ] Repair the tox test and have them checking before commit
