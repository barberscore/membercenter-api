# Local
from .base import *

DATABASES = {
    'default': dj_database_url.parse(
        get_env_variable("DATABASE_URL"),
        conn_max_age=600,
    ),
}

DATABASE_ROUTERS = []
