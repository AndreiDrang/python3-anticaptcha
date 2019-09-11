import asyncio

from python3_anticaptcha import CustomResultHandler


ANTICAPTCHA_KEY = ""
"""
This module is used to obtain the result of solving the task in "manual" mode
"""
TASK_ID = 123456

# prepare client
custom_result = CustomResultHandler.CustomResultHandler(
    anticaptcha_key=ANTICAPTCHA_KEY
)

response = custom_result.task_handler(task_id=TASK_ID)
print(response)


# async example
async def run():
    try:
        # io.IOBase
        custom_result = CustomResultHandler.aioCustomResultHandler(
            anticaptcha_key=ANTICAPTCHA_KEY
        )
        response = await custom_result.task_handler(task_id=TASK_ID)
        print(response)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()