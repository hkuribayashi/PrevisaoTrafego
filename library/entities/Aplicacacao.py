from enum import Enum


class Aplicacao(Enum):
    water_measurement = dict(estimated_quantity=1000.0, latency=1000.0, bandwidth=1.0, compression_factor=0.1,
                             start_adoption=15.0, adoption_rate=0.55)
    electricity_measurement = dict(estimated_quantity=1000.0, latency=1000.0, bandwidth=1.0, compression_factor=0.1,
                                   start_adoption=15.0, adoption_rate=0.55)
    ip_camera = dict(estimated_quantity=50.0, latency=10.0, bandwidth=25.0, compression_factor=1.0, start_adoption=10.0,
                     adoption_rate=0.45)
    other = dict(estimated_quantity=200.0, latency=10.0, bandwidth=2.0, compression_factor=1.0, start_adoption=5.0,
                 adoption_rate=0.55)
    enviromental_monitoring = dict(estimated_quantity=100.0, latency=1000.0, bandwidth=1.0, compression_factor=0.1,
                                   start_adoption=5.0, adoption_rate=0.45)
    e_health = dict(estimated_quantity=800.0, latency=1000.0, bandwidth=2.0, compression_factor=0.1, start_adoption=5.0,
                    adoption_rate=0.35)
    e_learning = dict(estimated_quantity=200.0, latency=10.0, bandwidth=8.0, compression_factor=1.0, start_adoption=5.0,
                      adoption_rate=0.55)
    web_browsing = dict(estimated_quantity=200.0, latency=60.0, bandwidth=2.0, compression_factor=1.0,
                        start_adoption=5.0, adoption_rate=0.55)
