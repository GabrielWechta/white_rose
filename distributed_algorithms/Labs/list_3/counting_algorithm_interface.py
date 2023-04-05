import abc


class CountingAlgorithmInterface(abc.ABC):

    @abc.abstractmethod
    def replace_data_stream(self, data_stream):
        pass

    @abc.abstractmethod
    def replace_M_length(self, M_length):
        pass

    @abc.abstractmethod
    def refresh_M(self):
        pass

    @abc.abstractmethod
    def consume_data_stream(self):
        pass

    @abc.abstractmethod
    def estimate_number_of_elements(self):
        pass
