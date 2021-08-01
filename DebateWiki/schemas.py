from schema import Or, Schema

config_schema = Schema(
    {
        "api": {
            "debug": Or(True, False),
            "log_level": Or(
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ),
            "jwt_secret": str,
            "database_url": str
        }
    }
)
