"""Constants for Diffazur Hydrocapt."""
# Base component constants


NAME = "Diffazur Hydrocapt"
DOMAIN = "diffazur_hydrocapt"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.0"
MANUFACTURER = "DIFFAZUR"

ATTRIBUTION = "Diffazur hydrocapt Data"
ISSUE_URL = "https://github.com/tmenguy/hacs-diffazur-hydrocapt/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
LIGHT = "light"
SELECT = "select"

PLATFORMS = [BINARY_SENSOR, SENSOR, LIGHT, SELECT]



# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
