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

__all__ = ('BlendAlphaCheckerboardPrimitive',)

Inputs = container.DataFrame

class Hyperparams(hyperparams.Hyperparams):

    nb_rows = hyperparams.Set[int](
        default=(4, 6),
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description='Number of rows of the checkerboard',
    )

    nb_cols = hyperparams.Set[int](
        default=(1, 4),
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description='Number of cols of the checkerboard',
    )

    seed = hyperparams.Constant[int](
        default=0,
        description='Minimum workers to extract frames simultaneously',
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
    )



class BlendAlphaCheckerboardPrimitive(AugmentationPrimitiveBase[Inputs, Hyperparams]):
    """
    A primitive which Blend images from two branches according to a checkerboard pattern.
    """

    metadata = construct_primitive_metadata("augmentation", "blend_BlendAlphaCheckerboard")

    def _get_function(self):
        """
        set up function and parameter of functions
        """
        nb_rows = self.hyperparams["nb_rows"]
        nb_cols = self.hyperparams["nb_cols"]
        seed = self.hyperparams["seed"]
        return iaa.BlendAlphaCheckerboard(nb_rows=nb_rows, nb_cols=nb_cols, seed=seed)

