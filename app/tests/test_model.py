import pytest
from src.models import AddressModel


def test_valid_data():
    """
    This function tests the correctness of the AddressModel class when given valid data.

    Parameters:
        data (dict): A dictionary containing the phone and address fields.

    Returns:
        None

    Raises:
        ValueError: If the phone number is not a valid phone number.

    """
    data = {"phone": "79831560972", "address": "Moscow City Street 28"}
    model = AddressModel(**data)
    assert model.phone == "79831560972"
    assert model.address == "Moscow City Street 28"


def test_invalid_phone():
    """
    This function tests the correctness of the AddressModel class when given invalid phone data.

    Parameters:
        data (dict): A dictionary containing the phone and address fields.

    Returns:
        None

    Raises:
        ValueError: If the phone number is not a valid phone number.

    """
    data = {"phone": "7983156097223", "address": "Moscow City Street 28"}
    try:
        model = AddressModel(**data)
    except ValueError as e:
        assert "Invalid phone number" in str(e)
