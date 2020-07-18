# TODO: Add support for Pandas.
# TODO: Create a method to test if node exists.
from powertools import config

import pyspark

import logging

logger = logging.getLogger(__name__)


class Node:
    """A reference to a DataFrame."""

    def __init__(
        self,
        path: str,
        root_path: str = config.ROOT_PATH,
    ):
        self.path = f'{root_path}{path}'

    def __repr__(self):
        return f'{self.__class__}(path={self.path})'

    def __str__(self):
        return self.path

    def __eq__(self, other):
        return self.path == other.path

    def __hash__(self):
        return hash(self.path)


class Output(Node):
    """Used for DataFrame Output of a Transform."""

    def __init__(
        self,
        path: str,
        base_path: str = config.BASE_PATH,
        root_path: str = config.ROOT_PATH,
        **write_kwargs
    ):
        super().__init__(path, base_path, root_path)
        self.write_kwargs = write_kwargs

    def save(self, df: pyspark.sql.DataFrame, **write_kwargs) -> None:
        """Save the ouput of a transform from a fixed path.

        The default save mode is set to 'overwrite' because this is most
        commonly used.

        Args:
            df (pyspark.sql.DataFrame): A DataFrame which is to be saved in the output
                location.
            **write_kwargs: The key value arguments to the DataFrameReader class
                in pyspark.sql.
        """
        write_kwargs = write_kwargs or self.write_kwargs
        if 'mode' not in write_kwargs:
            write_kwargs['mode'] = 'overwrite'
        df.write.save(path=self.path, **write_kwargs)


class Input(Node):
    """Used for DataFrame Input to a Transform."""

    def __init__(
        self,
        path: str,
        base_path: str = config.BASE_PATH,
        root_path: str = config.ROOT_PATH,
        **read_kwargs
    ):
        super().__init__(path, base_path, root_path)
        self.read_kwargs = read_kwargs

    def load(self, **read_kwargs) -> pyspark.sql.DataFrame:
        """Load the input of a transform from a fixed path.

        Args:
            **read_kwargs: Kwargs to the DataFrameReader class from pyspark.sql.

        Returns:
            pyspark.sql.DataFrame: The DataFrame that the input is pointing to.
        """
        spark = pyspark.sql.SparkSession.builder.getOrCreate()
        read_kwargs = read_kwargs or self.read_kwargs
        return spark.read.load(path=self.path, **read_kwargs)
