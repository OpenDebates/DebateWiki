from schema import Schema, Or

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
        }
    }
)
