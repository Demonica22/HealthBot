import logging


async def setup_logging():
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    logging.basicConfig(
        level=logging.INFO, format=format, datefmt="[%X]", handlers=[logging.StreamHandler()]
    )
