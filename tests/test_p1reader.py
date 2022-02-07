""" Test the p1reader module """
from unittest.mock import patch, MagicMock

import pytest

from p1reader import CRCException, P1Reader


@pytest.fixture(name="mock_serial")
def create_mock_serial() -> MagicMock:
    """Mock the Serial class used in P1Exporter"""
    with patch("p1reader.Serial") as mock:
        yield mock


def test_p1reader_init_defaults(mock_serial: MagicMock):
    """Test creation of a P1Exporter object with default values."""
    p1_reader = P1Reader()
    p1_reader.close()

    mock_serial.assert_called_with(
        port="/dev/ttyUSB0", baudrate=115200, xonxoff=1, timeout=1.0
    )


def test_p1reader_init_custom(mock_serial: MagicMock):
    """Test creation of a P1Exporter object with custom values."""
    p1_reader = P1Reader(device="/dev/foo")
    p1_reader.close()

    mock_serial.assert_called_with(
        port="/dev/foo", baudrate=115200, xonxoff=1, timeout=1.0
    )


def test_p1reader_raw_simple(mock_serial: MagicMock):
    """Test the raw() method with a simple dummy telegram"""
    fake_results = [b"/foo\r\n", b"bar\r\n", b"baz\r\n", b"!B587\r\n"]
    mock_serial.return_value.readline.side_effect = fake_results

    p1_reader = P1Reader()
    raw = p1_reader.raw().splitlines(keepends=True)
    p1_reader.close()

    for i, line in enumerate(fake_results[:-1]):
        assert raw[i] == line.decode("utf-8")

    assert mock_serial.return_value.readline.call_count == 4


def test_p1reader_raw_bad_crc(mock_serial: MagicMock):
    """Test a CRCException is raised when the CRC in the telegram is incorrect"""
    fake_results = [b"/foo\r\n", b"bar\r\n", b"baz\r\n", b"!1111\r\n"]
    mock_serial.return_value.readline.side_effect = fake_results

    p1_reader = P1Reader()
    with pytest.raises(CRCException):
        p1_reader.raw()

    p1_reader.close()


def test_p1reader_read(mock_serial):
    """Test the read() method with a real telegram"""
    with open("sample/fulllist.txt", "rb") as file:
        mock_serial.return_value.readline = file.readline

        p1_reader = P1Reader()
        telegram = p1_reader.read()
        p1_reader.close()

        assert telegram["0-0:96.1.4"] == "50216"
        assert telegram["0-0:96.1.1"] == "3153414731313030323932303039"
        assert telegram["0-0:1.0.0"] == "220125220702W"
        assert telegram["1-0:1.8.1"] == "000633.354"
        assert telegram["1-0:1.8.2"] == "000622.078"
        assert telegram["1-0:2.8.1"] == "000000.000"
        assert telegram["1-0:2.8.2"] == "000000.021"
        assert telegram["0-0:96.14.0"] == "0002"
        assert telegram["1-0:1.7.0"] == "00.334"
        assert telegram["1-0:2.7.0"] == "00.000"
        assert telegram["1-0:21.7.0"] == "00.334"
        assert telegram["1-0:22.7.0"] == "00.000"
        assert telegram["1-0:32.7.0"] == "244.4"
        assert telegram["1-0:31.7.0"] == "002.28"
        assert telegram["0-0:96.3.10"] == "1"
        assert telegram["0-0:17.0.0"] == "999.9"
        assert telegram["1-0:31.4.0"] == "999"
        assert telegram["0-0:96.13.0"] == ""
        assert telegram["0-1:24.1.0"] == "003"
        assert telegram["0-1:96.1.1"] == "37464C4F32313231303236323333"
        assert telegram["0-1:24.4.0"] == "1"
        assert telegram["0-1:24.2.3"] == "00871.525"


def test_p1reader_read_context_manager(mock_serial):
    """Test using P1Reader as a context manager"""
    with open("sample/fulllist.txt", "rb") as file:
        mock_serial.return_value.readline = file.readline

        with P1Reader() as p1_reader:
            telegram = p1_reader.read()

        assert telegram["0-0:96.1.4"] == "50216"
        assert mock_serial.return_value.close.call_count == 1


def test_p1reader_read_all(mock_serial: MagicMock):
    """Test the read() method reading multiple real telegrams"""
    with open("sample/fulllist.txt", "rb") as file:
        mock_serial.return_value.readline = file.readline

        with P1Reader() as p1_reader:
            for _ in range(7):
                p1_reader.read()
