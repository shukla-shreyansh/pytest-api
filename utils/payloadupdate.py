import random
import string
import re


class PayloadUpdate:

    @staticmethod
    def payloadupdate(payload, auto_update_keys=None, skip_keys=None):
        if auto_update_keys is None:
            auto_update_keys = {}

        if skip_keys is None:
            skip_keys = {'status', 'Type'}

        updated_payload = payload.copy()

        # Compile regex pattern for ID variations
        id_pattern = re.compile(r'id$|Id$|ID$|_id$|_Id$|_ID$', re.IGNORECASE)

        for key in updated_payload:
            # Skip if key contains any skip_keys or matches ID pattern
            if (any(skip_key.lower() in key.lower() for skip_key in skip_keys) or
                    id_pattern.search(key)):
                continue

            if key in auto_update_keys:
                update_func = auto_update_keys[key]
            else:
                update_func = PayloadUpdate.random_append

            try:
                # Validate key and value before updating
                if PayloadUpdate.is_valid_key_value(key, updated_payload[key]):
                    updated_payload[key] = update_func(updated_payload[key])
            except Exception as e:
                print(f"Failed to update key '{key}': {str(e)}")

        return updated_payload

    @staticmethod
    def random_append(value):
        try:
            if isinstance(value, str):
                # Filter out special characters and ensure the string is valid
                cleaned_value = ''.join(c for c in value if c.isprintable())
                random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
                return f"{cleaned_value}{random_string}"
            elif isinstance(value, (int, float)):
                return value + random.randint(1, 100)
            elif isinstance(value, bool):
                return not value
            elif isinstance(value, list):
                return value + [random.randint(1, 100)]
            elif isinstance(value, dict):
                return PayloadUpdate.payloadupdate(value)
            elif value is None:
                return None
            else:
                print(f"Unsupported value type: {type(value)}")
                return value
        except Exception as e:
            print(f"Error in random_append: {str(e)}")
            return value

    @staticmethod
    def is_valid_key_value(key, value):
        # Check if key contains only valid characters
        if not isinstance(key, str):
            print(f"Invalid key type: {type(key)}")
            return False

        # Check for invalid characters in key
        if not all(c.isprintable() for c in key):
            print(f"Key contains invalid characters: {key}")
            return False

        # Check if value is of supported type
        supported_types = (str, int, float, bool, list, dict, type(None))
        if not isinstance(value, supported_types):
            print(f"Unsupported value type for key '{key}': {type(value)}")
            return False

        return True