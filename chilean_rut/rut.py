import os
import re
from typing import Any
from pydantic_core import core_schema


class ChileanRut(str):
    """Custom type for handling Chilean RUT validation, formatting, and translation.

    Features:
        - Validates RUT format and check digit.
        - Cleans input by removing invalid characters.
        - Provides formatted representations (with/without dash or dots).
        - Supports dynamic translation of error messages and schema descriptions.
    """

    locale = os.getenv("RUT_LOCALE", "en")
    TRANSLATIONS = {
        "en": {
            "description": "Chilean RUT in format XXXXXXXX-Y. Validates and cleans the input.",
            "invalid_format": "Invalid RUT format.",
            "invalid_check_digit": "Invalid RUT check digit.",
        },
        "es": {
            "description": "RUT chileno en formato XXXXXXXX-Y. Valida y limpia el valor ingresado.",
            "invalid_format": "Formato de RUT inválido.",
            "invalid_check_digit": "Dígito verificador del RUT inválido.",
        },
    }

    def __new__(cls, rut: str) -> "ChileanRut":
        """Cleans and validates the RUT before creating an instance."""
        cleaned_rut = cls.clean_rut(rut)
        if not cls.is_valid_rut(cleaned_rut):
            raise ValueError(cls.translate("invalid_format"))
        return super().__new__(cls, cleaned_rut)

    def __init__(self, rut: str) -> None:
        self.rut = self.clean_rut(rut)

    def __str__(self) -> str:
        return self.rut

    @staticmethod
    def clean_rut(rut: str) -> str:
        """Cleans the RUT by removing invalid characters and converting to uppercase.

        Args:
            rut: The RUT string to clean.

        Returns:
            A cleaned RUT string.
        """
        return re.sub(r"[^0-9Kk]", "", rut).upper()

    @classmethod
    def is_valid_rut(cls, rut: str) -> bool:
        """Validates the RUT format and check digit.

        Args:
            rut: A cleaned RUT string.

        Returns:
            True if the RUT is valid, otherwise False.
        """
        if len(rut) < 2 or not re.match(r"^\d{5,8}[0-9K]$", rut):
            rtv = False
        else:
            number, verifier = rut[:-1], rut[-1]
            rtv = verifier == cls.calculate_verifier(number)
        return rtv

    @staticmethod
    def calculate_verifier(number: str) -> str:
        """Calculates the check digit for a given RUT number.

        Args:
            number: The numeric part of the RUT.

        Returns:
            The calculated check digit ('0'-'9' or 'K').
        """
        total = 0
        multiplier = 2
        for digit in reversed(number):
            total += int(digit) * multiplier
            multiplier = 2 if multiplier == 7 else multiplier + 1
        remainder = 11 - (total % 11)
        remainder = "0" if remainder == 11 else "K" if remainder == 10 else remainder
        return str(remainder)

    def with_dash(self) -> str:
        """Formats the RUT with a dash: XXXXXXXX-Y.

        Returns:
            The RUT formatted with a dash.
        """
        return f"{self.rut[:-1]}-{self.rut[-1]}"

    def with_dots(self) -> str:
        """Formats the RUT with dots and dash: XX.XXX.XXX-Y.

        Returns:
            The RUT formatted with dots and a dash.
        """
        number = self.rut[:-1]
        formatted_number = f"{int(number):,}".replace(",", ".")
        return f"{formatted_number}-{self.rut[-1]}"

    @classmethod
    def set_locale(cls, locale: str) -> None:
        """Sets the locale for translations.

        Args:
            locale: The locale string (e.g., 'en', 'es').

        Raises:
            ValueError: If the provided locale is not supported.
        """
        if locale not in cls.TRANSLATIONS:
            raise ValueError(f"Unsupported locale: {locale}")
        cls.locale = locale

    @classmethod
    def translate(cls, key: str) -> str:
        """Fetches a translated message based on the current locale.

        Args:
            key: The key for the message to translate.

        Returns:
            The translated message string.
        """
        return cls.TRANSLATIONS.get(cls.locale, cls.TRANSLATIONS["en"]).get(key, key)

    @classmethod
    def __get_validators__(cls):
        """Defines Pydantic validators."""
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "ChileanRut":
        """Validates the input value and returns a ChileanRut instance.

        Args:
            value: The input value to validate.

        Returns:
            A validated ChileanRut instance.

        Raises:
            TypeError: If the input value is not a string.
            ValueError: If the RUT format or check digit is invalid.
        """
        if not isinstance(value, str):
            raise TypeError(cls.translate("invalid_format"))
        if not cls.is_valid_rut(value):
            raise ValueError(cls.translate("invalid_check_digit"))
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        """Provides the core schema with translated descriptions.

        Args:
            _source_type: The source type for the schema (unused).
            _handler: The schema handler (unused).

        Returns:
            A CoreSchema instance for Pydantic v2.
        """
        description = cls.translate("description")

        def serialize(value: "ChileanRut", _info: core_schema.SerializationInfo) -> str:
            return str(value)

        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(
                # pattern=r"^\d{5,8}[0-9K]$", Not used as we allow uncleansed values
                metadata={"description": description}
            ),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(cls),
                    core_schema.chain_schema(
                        [
                            core_schema.str_schema(),
                            core_schema.no_info_plain_validator_function(cls.validate),
                        ]
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize, info_arg=True, return_schema=core_schema.str_schema()
            ),
        )
