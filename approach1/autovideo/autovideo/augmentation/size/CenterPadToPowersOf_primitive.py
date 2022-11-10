'''
Copyright 2021 D3M Team
Copyright (c) 2021 DATA Lab at Texas A&M University

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from d3m import container
from d3m.metadata import hyperparams
import imgaug.augmenters as iaa

from autovideo.utils import construct_primitive_metadata
from autovideo.base.augmentation_base import AugmentationPrimitiveBase

__all__ = ('CenterPadToPowersOfPrimitive',)

Inputs = container.DataFrame

class Hyperparams(hyperparams.Hyperparams):
    width_base = hyperparams.Hyperparameter[int](
        default=2,
        description='Base for the width.',
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
    )
    height_base = hyperparams.Hyperparameter[int](
        default=3,
        description='Base for the height.',
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
    )
    seed = hyperparams.Constant[int](
        default=0,
        description='Minimum workers to extract frames simultaneously',
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
    )



class CenterPadToPowersOfPrimitive(AugmentationPrimitiveBase[Inputs, Hyperparams]):
    """
    A primitive which pad images equally on all sides until H/W is a power of a base.
    """

    metadata = construct_primitive_metadata("augmentation", "size_CenterPadToPowersOf")

    def _get_function(self):
        """
        set up function and parameter of functions
        """
        seed = self.hyperparams["seed"]
        height_base = self.hyperparams["height_base"]
        width_base = self.hyperparams["width_base"]
        return iaa.CenterPadToPowersOf(width_base = width_base,height_base=height_base, seed=seed)
