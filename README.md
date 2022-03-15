# P1 Reader and Prometheus Exporter

A simple reader and Prometheus exporter to expose metric from Belgian/Dutch digital smart meters over the P1 port.

## Usage

```
$ pip install p1exporter
$ p1exporter
ts=2022-03-08T19:08:26 level=INFO caller=__main__ msg=Got telegram with 22 keys
ts=2022-03-08T19:08:27 level=INFO caller=__main__ msg=Got telegram with 22 keys
...

$ curl localhost:8080
...
# HELP p1_electricity_power_in_kw Instantaneous electricity power delivered to client (+P) in kW
# TYPE p1_electricity_power_in_kw gauge
p1_electricity_power_in_kw 0.511
# HELP p1_electricity_power_out_kw Instantaneous electricity power delivered by client (-P) in kW
# TYPE p1_electricity_power_out_kw gauge
p1_electricity_power_out_kw 0.0
...
```

```
>>> from p1exporter import P1Reader
>>> with P1Reader() as p1_reader:
...   p1_reader.read()
...
{'0-0:96.1.4': '50216', '0-0:96.1.1': '3153414731313030323932303039', '0-0:1.0.0': '220308191245W', '1-0:1.8.1': '000877.698', '1-0:1.8.2': '000841.449', '1-0:2.8.1': '000000.000', '1-0:2.8.2': '000000.021', '0-0:96.14.0': '0001', '1-0:1.7.0': '00.492', '1-0:2.7.0': '00.000', '1-0:21.7.0': '00.492', '1-0:22.7.0': '00.000', '1-0:32.7.0': '240.4', '1-0:31.7.0': '002.85', '0-0:96.3.10': '1', '0-0:17.0.0': '999.9', '1-0:31.4.0': '999', '0-0:96.13.0': '', '0-1:24.1.0': '003', '0-1:96.1.1': '37464C4F32313231303236323333', '0-1:24.4.0': '1', '0-1:24.2.3': '01225.316'}
```

## Todo

- Configurable serial device
- Configurable listen address:port
- List all metrics in README
- Tests for p1collector
- LICENSE

## References:

- https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf
- https://maakjemeterslim.be/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBclFDIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--6287e20f84bfe127b2c7687ff4e82e3f32394293/e-MUCS%20-%20P1%20v%201.4.pdf?disposition=attachment
- https://jensd.be/1183/linux/read-data-from-the-belgian-digital-meter-through-the-p1-port
