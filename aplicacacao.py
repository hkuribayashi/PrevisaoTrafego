import enum


class Aplicacao(enum.Enum):
    web_browsing = {'latency': 10.0, 'bandwidth': 2.0, 'compression_factor': 1.0}
    streaming_sd = {'latency': 10.0, 'bandwidth': 5.0, 'compression_factor': 1.0}
    streaming_hd = {'latency': 10.0, 'bandwidth': 25.0, 'compression_factor': 1.0}
