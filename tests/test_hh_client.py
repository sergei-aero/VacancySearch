import pytest
from unittest.mock import patch, Mock
from src.api.hh_client import HHClient
from requests.exceptions import RequestException


def test_get_employer_success():
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1455, "name": "HeadHunter"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.Session.get", return_value=mock_response) as mock_get:
        client = HHClient()
        result = client.get_employer(1455)
        assert result["name"] == "HeadHunter"
        mock_get.assert_called_once_with("https://api.hh.ru/employers/1455")


def test_get_employer_failure():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = RequestException("HTTP Error")
    with patch("requests.Session.get", return_value=mock_response):
        client = HHClient()
        result = client.get_employer(999999)
        assert result == {}


def test_get_vacancies_pagination():
    mock_response_page0 = Mock()
    mock_response_page0.json.return_value = {"items": [{"id": 1}], "pages": 2}
    mock_response_page1 = Mock()
    mock_response_page1.json.return_value = {"items": [{"id": 2}], "pages": 2}

    with patch("requests.Session.get") as mock_get:
        mock_get.side_effect = [mock_response_page0, mock_response_page1]
        client = HHClient()
        vacancies = client.get_vacancies(1455)
        assert len(vacancies) == 2
        assert mock_get.call_count == 2
