import os
import abc
import typing
from urllib.parse import urlparse

import pandas as pd
import torch
import torchvision

from d3m import container
from d3m.primitive_interfaces.base import *
from d3m.metadata import hyperparams, params

__all__ = ('SupervisedParamsBase', 'SupervisedHyperparamsBase', 'SupervisedPrimitiveBase',)

class SupervisedParamsBase(params.Params):
    model: typing.Optional[typing.Any]

class SupervisedHyperparamsBase(hyperparams.Hyperparams):
    load_pretrained = hyperparams.UniformBool(
        default=False,
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description="Controls whether loading pre-trained model"
    )

class SupervisedPrimitiveBase(PrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    """ A base for supervised learning for video racognition
    """
    def __init__(self, *, hyperparams: Hyperparams) -> None:
        super().__init__(hyperparams=hyperparams)

        self.tmp_dir = 'tmp'
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        # Use GPU if available
        if torch.cuda.is_available():
            print("--> Running on the GPU")
            self.device = torch.device("cuda:0")
        else:
            self.device = torch.device("cpu") 
            print("--> Running on the CPU")

    def get_params(self) -> Params:
        return SupervisedParamsBase(
            model = self.model,
        )

    def set_params(self, *, params: Params) -> None:
        self.model = params['model']

    def fit(self, *, timeout: float = None, iterations: int = None) -> CallResult[None]:
        """
        Fit the model with training data. Check whether we need fine-tune
        """
        self._init_model(pretrained = self.hyperparams['load_pretrained'])
        self._fit(timeout=timeout, iterations=iterations)

        return CallResult(None)
    
    def set_training_data(self, *, inputs: Inputs, outputs: Outputs) -> None:
        # right now only support one augmentation at one time
        self._augmentation = False
        if "augmentation" in list(inputs.columns):
            self._augmentation = inputs["augmentation"][0]
            inputs.drop("augmentation", axis=1, inplace=True) # drop augmentation

        self._transformation = False
        if "transformation" in list(inputs.columns):
            not_null_idx = inputs[inputs["transformation"].notnull()].index.tolist()
            transform_list = []
            for i in not_null_idx:
                transform_list.append(inputs["transformation"][i])
            self._transformation = torchvision.transforms.Compose(transform_list) 
            inputs.drop("transformation", axis=1, inplace=True) # drop augmentation

        self._inputs = inputs
        self._outputs = outputs
        self._frame_list = pd.concat([self._inputs, self._outputs], axis=1).to_numpy()

    @abc.abstractmethod
    def _fit(self, *, timeout: float = None, iterations: int = None):
        """
        Training
        """

    @abc.abstractmethod
    def _init_model(self, pretrained):
        """
        Initialize the model. Loading the weights if pretrained is True
        """

    @abc.abstractmethod
    def produce(self, *, inputs: container.DataFrame, timeout: float = None, iterations: int = None) -> CallResult[container.DataFrame]:
        """
        make the predictions
        """


