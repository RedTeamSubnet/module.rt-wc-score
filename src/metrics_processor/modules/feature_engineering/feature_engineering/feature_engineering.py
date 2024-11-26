from abc import ABC, abstractmethod

class FeatureEngineering(ABC):

    """
       Main FeatureEngineering class. This class is abstract class.
       All the feature engineering classes should inherit this class and implement process() method. 
    """
    @abstractmethod
    def process(self, *args, **kwargs):
        pass
