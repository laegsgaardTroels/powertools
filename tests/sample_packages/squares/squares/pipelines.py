from powertools import Pipeline
from squares import transforms

pipeline = Pipeline.discover_transforms(transforms)
