# custom_components/cleanprofs/const.py

# Integration domain used by Home Assistant to identify this integration.
DOMAIN = "cleanprofs"

# Config keys stored in the config entry.
CONF_ZIPCODE = "zipcode"
CONF_HOUSE_NUMBER = "house_number"

# Always create these 3 product sensors (user can disable unused ones).
FIXED_PRODUCTS = ["gft", "rest", "plastic"]

# CleanProfs API endpoint.
API_URL = "https://cleanprofs.jmsdev.nl/api/get-plannings-address"