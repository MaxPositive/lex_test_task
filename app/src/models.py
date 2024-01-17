from pydantic import BaseModel, field_validator


class AddressModel(BaseModel):
    """
    A Pydantic model for an address.

    Attributes:
        phone: The phone number of the address.
        address: The street address of the address.
    """

    phone: str
    address: str

    @field_validator("phone")
    def validate_phone(cls, value: str) -> str:
        """
        Validate the phone number.

        Args:
            value (str): The phone number to validate.

        Raises:
            ValueError: If the phone number is not valid.

        Returns:
            str: The validated phone number.
        """
        if not value.isdigit() or (len(value) != 11):
            raise ValueError(
                "Invalid phone number. It should be 11 digits and consist only with digits."
            )
        return value
