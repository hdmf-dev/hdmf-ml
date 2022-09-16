from hdmf.utils import docval, popargs
from hdmf.common import get_class, register_class, DynamicTable
from hdmf.container import Container
import numpy as np
from sklearn.preprocessing import LabelEncoder


@register_class('ResultsTable', 'hdmf-ml')
class ResultsTable(get_class('ResultsTable', 'hdmf-ml')):

    @docval({'name': 'cls',         'type': (str, type), 'doc': 'data for this column'},
            {'name': 'data',        'type': 'array_data', 'doc': 'data for this column'},
            {'name': 'name',        'type': str,     'doc': 'the name of this column'},
            {'name': 'description', 'type': str,     'doc': 'a description for this column'},
            allow_extra=True)
    def __add_col(self, **kwargs):
        cls, data, name, description = popargs('cls', 'data', 'name', 'description', kwargs)
        if len(self.id) < len(data):
            self.id.extend(np.arange(len(self.id), len(data)))
        if isinstance(cls, str):
            cls = get_class(cls, 'hdmf-ml')
        self.add_column(data=data, name=name, description=description, **kwargs)

    @docval({'name': 'data',        'type': 'array_data', 'doc': 'data for this column'},
            {'name': 'name',        'type': str,     'doc': 'the name of this column', 'default': 'tvt_split'},
            {'name': 'description', 'type': str,     'doc': 'a description for this column', 'default': 'train/validation/test mask'})
    def add_tvt_split(self, **kwargs):
        """Add mask of 0, 1, 2 indicating which samples were used for trainingi validation, and testing."""
        kwargs['enum'] = ['train', 'validate', 'test']
        ret = self.__add_col('TrainValidationTestSplit', **kwargs)


    @docval({'name': 'data',        'type': 'array_data', 'doc': 'train-validation-test split data'},
            {'name': 'name',        'type': str,     'doc': 'the name of this column', 'default': 'tvt_split'},
            {'name': 'description', 'type': str,     'doc': 'a description for this column', 'default': "cross-validation split labels"})
    def add_cv_split(self, **kwargs):
        """Add cross-validation split mask"""
        self.__add_col("CrossValidationSplit", **kwargs)

    @docval({'name': 'data',        'type': 'array_data', 'doc': 'ground truth labels for each sample'},
            {'name': 'name',        'type': str,     'doc': 'the name of this column', 'default': 'true_label'},
            {'name': 'description', 'type': str,     'doc': 'a description for this column', 'default': 'ground truth labels'})
    def add_true_label(self, **kwargs):
        """Add ground truth labels for each sample"""
        if isinstance(kwargs['data'][0], (bytes, str)):
            enc = LabelEncoder()
            kwargs['data'] = enc.fit_transform(kwargs['data'])
            kwargs['enum'] = enc.classes_
        self.__add_col('VectorData', **kwargs)

    @docval({'name': 'data',        'type': 'array_data', 'doc': 'probability of sample for each class'},
            {'name': 'name',        'type': str,     'doc': 'the name of this column', 'default': 'predicted_probability'},
            {'name': 'description', 'type': str,     'doc': 'a description for this column', 'default': "the probability of the predicted class"})
    def add_predicted_probability(self, **kwargs):
        """Add probability of the sample for each class in the model"""
        self.__add_col('ClassProbability', **kwargs)

    @docval({'name': 'data',        'type': 'array_data', 'doc': 'predicted class lable for each sample'},
            {'name': 'name',        'type': str,     'doc': 'the name of this column', 'default': 'predicted_class'},
            {'name': 'description', 'type': str,     'doc': 'a description for this column', 'default': "the predicted class"})
    def add_predicted_class(self, **kwargs):
        """Add predicted class label for each sample"""
        self.__add_col('ClassLabel', **kwargs)

    @docval({'name': 'data',        'type': 'array_data', 'doc': 'predicted value for each sample'},
            {'name': 'name',        'type': str,     'doc': 'the name of this column', 'default': 'predicted_value'},
            {'name': 'description', 'type': str,     'doc': 'a description for this column', 'default': "the predicted regression output"})
    def add_predicted_value(self, **kwargs):
        """Add predicted value (i.e. from a regression model) for each sample"""
        self.__add_col('RegressionOutput', **kwargs)

    @docval({'name': 'data',        'type': 'array_data', 'doc': 'cluster label for each sample'},
            {'name': 'name',        'type': str,     'doc': 'the name of this column', 'default': 'cluster_label'},
            {'name': 'description', 'type': str,     'doc': 'a description for this column', 'default': "labels after clustering"})
    def add_cluster_label(self, **kwargs):
        """Add cluster label for each sample"""
        self.__add_col('ClusterLabel', **kwargs)

    @docval({'name': 'data',        'type': 'array_data', 'doc': 'embedding of each sample'},
            {'name': 'name',        'type': str,     'doc': 'the name of this column', 'default': 'embedding'},
            {'name': 'description', 'type': str,     'doc': 'a description for this column', 'default': "dimensionality reduction outputs"})
    def add_embedding(self, **kwargs):
        """Add embedding (a.k.a. transformation or representation) of each sample"""
        self.__add_col('EmbeddedValues', **kwargs)

    @docval({'name': 'data',        'type': 'array_data', 'doc': 'top-k predicted classes for each sample'},
            {'name': 'name',        'type': str,     'doc': 'the name of this column', 'default': 'topk_classes'},
            {'name': 'description', 'type': str,     'doc': 'a description for this column', 'default': "the top k predicted classes"})
    def add_topk_classes(self, **kwargs):
        """Add the top *k* predicted classes for each sample"""
        self.__add_col('TopKClasses', **kwargs)

    @docval({'name': 'data',        'type': 'array_data', 'doc': 'probabilities of the top-k predicted classes for each sample'},
            {'name': 'name',        'type': str,     'doc': 'the name of this column', 'default': 'topk_probabilities'},
            {'name': 'description', 'type': str,     'doc': 'a description for this column', 'default': "the probabilityes of the top k predicted classes"})
    def add_topk_probabilities(self, **kwargs):
        """Add probabilities for the top *k* predicted classes for each sample"""
        self.__add_col('TopKProbabilities', **kwargs)
