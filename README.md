# Chilean Rut

**ChileanRut** is a custom Python type for validating, formatting, and translating Chilean RUTs (Rol Único Tributario). It cleans the input, validates both the format and check digit, and provides formatted representations—with or without dashes and dots. It also supports dynamic error message translations and integrates seamlessly with [Pydantic](https://pydantic-docs.helpmanual.io/) for model validation.

## Features

- **Validation:** Checks RUT format and validates the check digit.
- **Cleaning:** Removes extraneous characters and converts the input to a standardized uppercase format.
- **Formatting:** Provides helper methods to display the RUT with a dash (`with_dash()`) or with dots and dash (`with_dots()`).
- **Localization:** Supports multiple locales (e.g., English and Spanish) for error messages and schema descriptions.
- **Pydantic Integration:** Implements custom validators to be used directly in Pydantic models.

## Installation

Install via pip

```bash
pip install k-chilean-rut
```

## Usage Examples

### Basic usage

```python
from chilean_rut import ChileanRut

# Create a ChileanRut instance (input can be uncleaned)
rut = ChileanRut("12.345.678-5")
print(rut)              # Outputs the cleaned RUT, e.g., "123456785"
print(rut.with_dash())  # Outputs "12345678-5"
print(rut.with_dots())  # Outputs "12.345.678-5"
```

### Pydantic usage

```python
from pydantic import BaseModel
from chilean_rut import ChileanRut

class User(BaseModel):
    name: str
    rut: ChileanRut

# Pydantic will use the custom validators defined in ChileanRut
user = User(name="Lucho", rut="123456785")
print(user.rut.with_dash())  # "12345678-5"

```

---

## License

This project is licensed under the KSL License for **free public use**. See the [LICENSE](LICENSE) file for details or [Web LICENSE](https://kimia.lat/license)