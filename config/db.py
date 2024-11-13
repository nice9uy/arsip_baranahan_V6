import logging
from .config import client
from colorama import Fore, Style
from pymongo.collection import Collection
from .config import collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def connect_to_mongodb():
    try:
        client.admin.command("ping")
        logger.info(Fore.GREEN + "Berhasil connect ke MongoDB." + Style.RESET_ALL)

    except Exception as e:
        logger.error(Fore.RED + "Gagal connect ke MongoDB: %s", e + Style.RESET_ALL)
        client.close()


def get_collection() -> Collection:
    return collection
