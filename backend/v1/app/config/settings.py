"""LibookTrac Backend System Settings and Configurations."""

import os

from dotenv import load_dotenv


def get_database_url():
    load_dotenv()
    url = os.getenv("DATABASE_URL",
                    "postgresql://postgres:password@libooktrac-db:5432/libooktrac")
    if url is None:
        raise ValueError("DATABASE_URL environment variable is not set.")
    return url