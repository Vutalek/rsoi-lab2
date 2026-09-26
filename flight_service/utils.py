import os

from sqlalchemy import create_engine

def construct_engine():
    protocol = os.environ.get("FLIGHT_SERVICE_DB_PROTOCOL", "")
    user = os.environ.get("FLIGHT_SERVICE_DB_USER", "")
    password = os.environ.get("FLIGHT_SERVICE_DB_PASSWORD", "")
    host = os.environ.get("FLIGHT_SERVICE_DB_HOST", "")
    port = os.environ.get("FLIGHT_SERVICE_DB_PORT", "")
    name = os.environ.get("FLIGHT_SERVICE_DB_NAME", "")

    return create_engine(
        f"{protocol}://{user}:{password}@{host}:{port}/{name}"
    )