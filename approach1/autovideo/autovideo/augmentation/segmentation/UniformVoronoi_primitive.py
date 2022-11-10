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
import typing
from autovideo.utils import construct_primitive_metadata
from autovideo.base.augmentation_base import AugmentationPrimitiveBase

__all__ = ('UniformVoronoiPrimitive',)

Inputs = container.DataFrame

class Hyperparams(hyperparams.Hyperparams):
    n_points = hyperparams.Hyperparameter[typing.Union[int,tuple,list]](
        default=(50,500),
        description='Number of points to sample on each image.',
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
    )

    p_replace = hyperparams.Hyperparameter[typing.Union[float,tuple,list]](
        default=(0.5,1.0),
        description='Defines for any segment the probability that the pixels within that segment are replaced by their average color (otherwise, the pixels are not changed).  ',
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
    )

    max_size = hyperparams.Hyperparameter[typing.Union[int,None]](
        default=128,
        description='Maximum image size at which the augmentation is performed. ',
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
    )

    seed = hyperparams.Constant[int](
        default=0,
        description='Minimum workers to extract frames simultaneously',
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
    )


class UniformVoronoiPrimitive(AugmentationPrimitiveBase[Inputs, Hyperparams]):
    """
    A primitive which Uniformly sample Voronoi cells on images and average colors within them.
    """

    metadata = construct_primitive_metadata("augmentation", "segmentation_UniformVoronoi")

    def _get_function(self):
        """
        set up function and parameter of functions
        """
        seed = self.hyperparams["seed"]
        n_points = self.hyperparams["n_points"]
        p_replace = self.hyperparams["p_replace"]
        max_size = self.hyperparams["max_size"]

        return iaa.UniformVoronoi(n_points=n_points,p_replace = p_replace ,max_size=max_size,seed=seed)