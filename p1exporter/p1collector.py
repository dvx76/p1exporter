""" TODO """
from typing import Mapping

from prometheus_client.core import (
    InfoMetricFamily,
    GaugeMetricFamily,
    CounterMetricFamily,
)

# TODO
# - logger
# - debug
# - click


class P1Collector:
    def __init__(self):
        """TODO"""
        self._setup_metrics()

    def _setup_metrics(self):
        self._prometheus_metrics = {
            "0-0:1.0.0": InfoMetricFamily(
                name="p1_date_of_message",
                documentation="Date-time stamp of the P1 message",
            ),
            "0-0:17.0.0": InfoMetricFamily(
                name="p1_electricity_threshold_kw",
                documentation="Actual threshold electricity in kW",
            ),
            "1-0:31.4.0": InfoMetricFamily(
                name="p1_electricity_threshold_amp",
                documentation="Actual threshold electricity in A",
            ),
            "0-0:96.1.1": InfoMetricFamily(
                name="p1_equipment_identifier", documentation="Equipment identifier"
            ),
            "0-0:96.3.10": GaugeMetricFamily(
                name="p1_electricity_switch_position",
                documentation="Switch position electricity",
            ),
            "0-0:96.1.4": InfoMetricFamily(
                name="p1_version_information", documentation="Version Information"
            ),
            "0-0:96.13.0": InfoMetricFamily(
                name="p1_text_message", documentation="Text message"
            ),
            "0-0:96.14.0": GaugeMetricFamily(
                name="p1_current_tariff_indicator",
                documentation="Tariff indicator electricity",
            ),
            "0-1:24.1.0": InfoMetricFamily(
                name="p1_other_devices_on_bus", documentation="Other devices on bus"
            ),
            "0-1:24.4.0": GaugeMetricFamily(
                name="p1_gas_switch_position",
                documentation="Switch position natural gas",
            ),
            "0-1:24.2.3": CounterMetricFamily(
                name="p1_gas_meter_m3_total",
                documentation="Reading from natural gas meter (in m3)",
            ),
            "0-1:96.1.1": InfoMetricFamily(
                name="p1_gas_meter_serial_numer",
                documentation="Serial number of natural gas meter in ASCII hex",
            ),
            "1-0:1.7.0": GaugeMetricFamily(
                name="p1_electricity_power_in_kw",
                documentation="Instantaneous electricity power delivered to client (+P) in kW",
            ),
            "1-0:2.7.0": GaugeMetricFamily(
                name="p1_electricity_power_out_kw",
                documentation="Instantaneous electricity power delivered by client (-P) in kW",
            ),
            "1-0:1.8.1": CounterMetricFamily(
                name="p1_electricity_meter_tariff1_in_kwh_total",
                documentation="Meter Reading electricity delivered to client (Tariff 1) in kWh",
            ),
            "1-0:1.8.2": CounterMetricFamily(
                name="p1_electricity_meter_tariff2_in_kwh_total",
                documentation="Meter Reading electricity delivered to client (Tariff 2) in kWh",
            ),
            "1-0:2.8.1": CounterMetricFamily(
                name="p1_electricity_meter_tariff1_out_kwh_total",
                documentation="Meter Reading electricity delivered by client (Tariff 1) in kWh",
            ),
            "1-0:2.8.2": CounterMetricFamily(
                name="p1_electricity_meter_tariff2_out_kwh_total",
                documentation="Meter Reading electricity delivered by client (Tariff 2) in kWh",
            ),
            "1-0:21.7.0": GaugeMetricFamily(
                name="p1_electricity_power_l1_in_kw",
                documentation="Instantaneous electricity power L1 delivered to client (+P) in kW",
            ),
            "1-0:22.7.0": GaugeMetricFamily(
                name="p1_electricity_power_l1_out_kw",
                documentation="Instantaneous electricity power L1 delivered by client (+P) in kW",
            ),
            "1-0:31.7.0": GaugeMetricFamily(
                name="p1_electricity_power_l1_amp",
                documentation="Instantaneous electricity current L1 in A",
            ),
            "1-0:32.7.0": GaugeMetricFamily(
                name="p1_electricity_power_l1_volt",
                documentation="Instantaneous voltage L1 in V",
            ),
        }

    def collect(self):
        """Called when exporter receives a request"""
        for metric in self._prometheus_metrics.values():
            yield metric

    def update(self, telegram: Mapping[str, str]):
        """Update prometheus_metrics with data from telegram"""
        self._setup_metrics()
        for code, value in telegram.items():
            if code in self._prometheus_metrics:
                if isinstance(self._prometheus_metrics[code], InfoMetricFamily):
                    self._prometheus_metrics[code].add_metric(
                        labels=[], value={"value": value}
                    )
                else:
                    self._prometheus_metrics[code].add_metric(labels=[], value=value)
            else:
                print(f"Collector does not know about {code}.")
