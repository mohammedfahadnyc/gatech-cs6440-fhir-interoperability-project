from pathlib import Path
from typing import Callable, TypeVar, Union

import pandas as pd
from torch.utils.data import Dataset

from ml_fhir.transforms import Transform

T = TypeVar("T")

class StrokeDataset(Dataset):
    def __init__(
            self,
            annotation_file: Union[str, None],
            features_file: Union[str, None],
            transform: Union[Callable, Transform, None]= None,
            target_transform: Union[Callable, Transform, None] = None,
        ) -> None:
        self._labels = pd.read_csv(annotation_file)
        self._features = pd.read_csv(features_file)
        self._transform = transform
        self._target_transform = target_transform
    
    def __getitem__(self, index: int) -> T:
        feature = self._features.iloc[index]
        label = self._labels.iloc[index]
        if self._transform:
            feature = self._transform(feature)
        if self._target_transform:
            label = self._target_transform(label)
        return feature, label
    
    def __len__(self) -> int:
        return len(self._features)
