import abc

class DynamoDBModel(abc.ABC):

    @abc.abstractmethod
    def save():
        pass
    
    @abc.abstractmethod
    def get():
        pass