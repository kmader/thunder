from thunder.rdds.series import Series
from thunder.rdds.images import Images

from numpy import asarray


class FeatureMethod(object):
    """
    Extract sources from spatiotemporal data using featue detection methods.

    A feature method first process the raw data to compute a single image or volume,
    and then uses an algorithm to extract sources. It requires three components:
    a preprocessor (which process the raw data)
    an algorithm (which extracts sources from the resulting image or volume)
    and a cleaner (which filters the output and removes bad sources)

    Parameters
    ----------
    algorithm : FeatureAlgorithm
        Which algorithm to use

    preprocessor : FeatureProcessor
        Which preprocessor to use

    kwargs : dict
        Any extra arguments will be passed to the algorithm, merger, and cleaner,
        useful for providing options to these components
    """

    def __init__(self, algorithm=None, preprocessor=None, cleaner=None, **kwargs):

        from thunder.extraction.cleaners import BasicCleaner

        self.preprocessor = preprocessor
        self.algorithm = algorithm
        self.cleaner = cleaner if cleaner is not None else BasicCleaner(**kwargs)

    def fit(self, data):
        """
        Fit the source extraction model to data.

        Distributed objects (Images or Series) must be preprocessed to obtain
        an image or volume on which to apply algorithms. Alternatively,
        an image or volume can be provided directly.

        Parameters
        ----------
        data : Images, Series, or array-like
            Data in either an images or series representation
        """

        if not isinstance(self.algorithm, FeatureAlgorithm):
            raise Exception("A FeatureAlgorithm must be specified")

        if isinstance(data, Images) or isinstance(data, Series):

            if not isinstance(self.preprocessor, FeaturePreprocessor):
                raise Exception("A FeaturePreprocessor must be specified")

            input = self.preprocessor.preprocess(data)

        else:
            try:
                input = asarray(data)
            except:
                raise Exception("Cannot interpret input")

        model = self.algorithm.extract(input)
        model = self.cleaner.clean(model)

        return model


class FeaturePreprocessor(object):
    """
    Process a Series or Images object into an array on which to apply algorithm
    """
    def preprocess(self, data):
        raise NotImplementedError


class FeatureAlgorithm(object):
    """
    Extract sources from a 2D or 3D array
    """

    def extract(self, im):
        raise NotImplementedError

