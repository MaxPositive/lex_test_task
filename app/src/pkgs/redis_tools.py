from redis.asyncio import Redis


class RedisTools:
    """
    A class for interacting with Redis.

    Args:
        host (str): The hostname or IP address of the Redis server.
        port (int): The port number of the Redis server.
    """

    __redis_connect = Redis(host="redis", port=6379)

    @classmethod
    async def save_address(cls, phone: str, address: str) -> None:
        """
        Save an address in Redis.

        Args:
            phone (str): The phone number of the customer.
            address (str): The address to be saved.
        """
        await cls.__redis_connect.set(phone, address)

    @classmethod
    async def get_address(cls, phone: str) -> str:
        """
        Retrieve an address from Redis.

        Args:
            phone (str): The phone number of the customer.

        Returns:
            The address associated with the given phone number, or None if no address is found.
        """
        return await cls.__redis_connect.get(phone)

    @classmethod
    async def delete_address(cls, phone: str) -> None:
        """
        Delete an address from Redis.

        Args:
            phone (str): The phone number of the customer.
        """
        await cls.__redis_connect.delete(phone)


redis_tools = RedisTools()
