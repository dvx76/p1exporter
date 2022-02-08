""" A simple module to read telegrams from a P1 port over a serial connection """

import logging
from typing import Mapping
from crcmod.predefined import mkPredefinedCrcFun
from serial import Serial

crc16 = mkPredefinedCrcFun("crc16")

logger = logging.getLogger(__name__)


class CRCException(Exception):
    """TODO"""


class P1Reader:
    """Wrap Serial and provide methods to read telegrams from a P1 connection

    Example:

    from p1reader import P1Reader
    p1_reader = P1Reader()
    telegram = p1_reader.read()
    print(telegram["1-0:1.8.1"])
    p1_reader.close()

    with P1Reader as p1_reader:
        telegram = p1_reader.read()
    """

    def __init__(self, device: str = "/dev/ttyUSB0"):
        self.device = device
        self._serial = Serial(port=self.device, baudrate=115200, xonxoff=1, timeout=1.0)

    def raw(self) -> str:
        """Returns a single utf-8 decoded P1 telegram.

        The first line of a P1 telegram is "/" + the meter identifier.
        The last line of a P1 telegram is "!" + the checksum of the telegram.

        Not using Serial.read_until() which doesn't seem to work very well
        """
        line: bytes = b""
        telegram: bytes = b""
        while True:
            line = self._serial.readline()
            if line.startswith(b"/"):
                telegram = b""
            if line.startswith(b"!"):
                break
            telegram += line

        logger.debug(f"telegram is {telegram}")
        checksum_calculated = crc16(telegram + b"!")
        checksum_expected = int("0x" + line.decode("utf-8")[1:], 16)
        if checksum_calculated != checksum_expected:
            raise CRCException(
                f"Invalid checksum {checksum_calculated} != {checksum_expected}"
            )

        return telegram.decode("utf-8")

    def read(self) -> Mapping[str, str]:
        """Returns a single P1 telegram as a dictionary with the OBIS code as key
        and the units stripped from the values. All values are strings.

        Example:
        {
            "0-0:96.1.4": "50216",
            "0-0:96.1.1": "3153414731313030323932303039",
            "1-0:1.7.0": "00.334"
            ...
        }
        """
        telegram = self.raw()
        processed_telegram: Mapping[str, str] = {}
        for line in telegram.splitlines():

            value: str = ""
            split_line = line.split("(")
            if len(split_line) == 1:
                logger.debug(f"Skipping line: {line}")
            code = split_line[0]

            try:
                value = split_line[1].rstrip(")")
                if len(split_line) == 3:
                    value = split_line[2].rstrip(")")
                processed_telegram[code] = self._strip_unit(value)
            except IndexError:
                continue

        return processed_telegram

    def close(self):
        """Close the wrapped Serial object"""
        self._serial.close()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    @staticmethod
    def _strip_unit(value: str) -> str:
        """Strip the unit from a value.

        E.g. "00871.525*m3" -> "00871.525"
        """
        return value.split("*")[0]
