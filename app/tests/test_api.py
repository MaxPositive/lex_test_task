import asyncio

import pytest
from httpx import AsyncClient
from fastapi import status
from src.main import app


pytestmark = pytest.mark.asyncio(scope="module")

loop: asyncio.AbstractEventLoop


async def test_write_address() -> None:
    """
    This function tests the write_address endpoint of the FastAPI application.

    It sends a POST request with sample data to the /addresses endpoint to create a new address,
    and finally sends a GET request with the same phone number to the /addresses endpoint to
    ensure that the address was created successfully.

    Parameters:
        None

    Returns:
        None
    """
    global loop
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Send a POST request with sample data to the /addresses endpoint to create a new address
        response = await client.post(
            "/addresses", json={"phone": "89090000000", "address": "123 Main St"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"status": "Address written successfully"}

        # Send a GET request with the same phone number to the /addresses endpoint to
        # ensure that the address was created successfully
        address = await client.get(
            "/addresses?phone=89090000000",
        )
        assert address.status_code == status.HTTP_200_OK
        assert address.json()["address"] == "123 Main St"


async def test_address_already_exists() -> None:
    """
    This function tests the address_already_exists endpoint of the FastAPI application.

    It sends a POST request with sample data to the /addresses endpoint to create a new address,
    and ensures that the response code is 409 Conflict and the response body contains the error message
    "Address already exists".

    Parameters:
        None

    Returns:
        None
    """
    global loop
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(
            "/addresses", json={"phone": "89090000000", "address": "123 Main St"}
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {"detail": "Address already exists"}


async def test_read_address() -> None:
    """
    This function tests the read_address endpoint of the FastAPI application.

    It sends a GET request to the /addresses endpoint with a phone number as a query parameter,
    and ensures that the response code is 200 OK and the response body contains the address associated with the phone number.

    Parameters:
        None

    Returns:
        None
    """
    global loop
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get(
            "/addresses?phone=89090000000",
        )
        assert response.status_code == status.HTTP_200_OK


async def test_update_address() -> None:
    """
    This function tests the update_address endpoint of the FastAPI application.

    It sends a GET request to the /addresses endpoint with the phone number as a query parameter,
    and ensures that the response code is 200 OK and the response body contains the address associated with the phone number.
    If the address does not exist, it will return a 404 Not Found error.

    Then, it sends a PUT request with the updated address information to the /addresses endpoint,
    and ensures that the response code is 200 OK and the response body contains the status message "Address updated successfully".

    Parameters:
        None

    Returns:
        None
    """
    global loop
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        first_address = await client.get(
            "/addresses?phone=89090000000",
        )
        assert first_address.status_code == status.HTTP_200_OK
        response = await client.put(
            "/addresses", json={"phone": "89090000000", "address": "124 Main St"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "Address updated successfully"}
        second_address = await client.get(
            "/addresses?phone=89090000000",
        )
        assert second_address.status_code == status.HTTP_200_OK
        assert second_address.json()["address"] == "124 Main St"


async def test_delete_address() -> None:
    """
    This function tests the delete_address endpoint of the FastAPI application.

    It sends a GET request to the /addresses endpoint with the phone number as a query parameter,
    and ensures that the response code is 200 OK and the response body contains the address associated with the phone number.
    Then, it sends a DELETE request to the /addresses endpoint with the same phone number,
    and ensures that the response code is 204 No Content and the response body is empty.
    Finally, it sends a GET request to the /addresses endpoint with the same phone number again,
    and ensures that the response code is 404 Not Found and the response body contains the error message "Address not found".

    Parameters:
        None

    Returns:
        None
    """
    global loop
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/addresses?phone=89090000000")
        assert response.status_code == status.HTTP_200_OK
        response = await client.delete("/addresses?phone=89090000000")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = await client.get("/addresses?phone=89090000000")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Address not found"


async def test_update_address_failed() -> None:
    """
    This function tests the update_address endpoint of the FastAPI application.

    It sends a PUT request to the /addresses endpoint with the phone number and address as a body parameter,
    and ensures that the response code is 404 Not Found if the address does not exist.

    Parameters:
        None

    Returns:
        None
    """
    global loop
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.put(
            "/addresses", json={"phone": "89090000000", "address": "124 Main St"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_read_address_failed() -> None:
    """
    This function tests the update_address endpoint of the FastAPI application.

    It sends a GET request to the /addresses endpoint with the phone number as a query parameter,
    and ensures that the response code is 404 Not Found if the address does not exist.

    Parameters:
        None

    Returns:
        None
    """
    global loop
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get(
            "/addresses?phone=89090000000",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
