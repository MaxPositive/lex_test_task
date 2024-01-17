from typing import Dict, Annotated
from fastapi import FastAPI, status, HTTPException
from fastapi import Query, Body
from src.models import AddressModel
from src.pkgs.redis_tools import redis_tools

app = FastAPI()


@app.delete("/addresses", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(phone: str = Query(...)) -> None:
    """
    Delete an address from Redis.
    :param phone: phone number of the customer.
    :return: None
    """
    await redis_tools.delete_address(phone)


@app.post("/addresses", status_code=status.HTTP_201_CREATED)
async def write_address(address: AddressModel = Body(...)) -> Dict[str, str]:
    """
    Write an address in Redis.
    :param address: AddressModel consisting of phone number and address.
    :return: message of success save.
    """
    if await redis_tools.get_address(address.phone) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Address already exists"
        )
    await redis_tools.save_address(address.phone, address.address)
    return {"status": "Address written successfully"}


@app.put("/addresses", status_code=status.HTTP_200_OK)
async def update_address(address: AddressModel = Body(...)) -> Dict[str, str]:
    """
    Update an address in Redis.
    :param address: AddressModel consisting of phone number and address.
    :return: message of success update.
    """
    if await redis_tools.get_address(address.phone) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    await redis_tools.save_address(address.phone, address.address)
    return {"status": "Address updated successfully"}


@app.get("/addresses", status_code=status.HTTP_200_OK)
async def read_address(phone: str = Query(...)) -> Dict[str, Annotated[str, None]]:
    """
    Read an address from Redis.
    :param phone: phone number of the customer.
    :return: address of the customer.
    """
    address = await redis_tools.get_address(phone)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    return {"address": address}
