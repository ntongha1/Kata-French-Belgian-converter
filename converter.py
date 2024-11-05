class FrenchNumberTranslator:
    """
    FrenchNumberTranslator is a class designed to convert non-negative integers into their French
    word equivalents. It supports conversion for numbers ranging from 0 to 999,999.

    Attributes:
        lang (str): The language variant for conversion. Default is "fr" (French).
                    Another supported option is Belgian French, indicated by "be".

    Methods:
        convert_number(n: int) -> str:
            Converts a given non-negative integer n into its French word equivalent.
            Raises a ValueError if n is not a non-negative integer or is out of the supported range.

    Usage Example:
        converter = FrenchNumberTranslator()
        print(converter.convert_number(123))  # Outputs: "cent-vingt-trois"

        belgian_converter = FrenchNumberTranslator(lang="be")
        print(belgian_converter.convert_number(123))  # Outputs the Belgian French equivalent
    """

    def __init__(self, lang: str = "fr") -> None:
        self.lang = lang

        # Base number mappings
        self.units = [
            "zéro",
            "un",
            "deux",
            "trois",
            "quatre",
            "cinq",
            "six",
            "sept",
            "huit",
            "neuf",
        ]
        self.teens = ["dix", "onze", "douze", "treize", "quatorze", "quinze", "seize"]

        if self.lang == "fr":
            self.tens = [
                "",
                "dix",
                "vingt",
                "trente",
                "quarante",
                "cinquante",
                "soixante",
            ]
            self.special_tens = {
                70: "soixante-dix",
                71: "soixante-et-onze",
                80: "quatre-vingts",
                90: "quatre-vingt-dix",
            }
        elif self.lang == "be":
            self.tens = [
                "",
                "dix",
                "vingt",
                "trente",
                "quarante",
                "cinquante",
                "soixante",
                "septante",
                "huitante",
                "nonante",
            ]
        else:
            raise ValueError(f"Unsupported language variant: {lang}. Supported variants are 'fr' and 'be'.")

    def _handle_tens(self, n):
        """Helper method to handle tens and units."""
        if n % 10 == 0:
            return self.tens[n // 10]
        if n % 10 == 1 and n != 11:
            return self.tens[n // 10] + "-et-un"
        return self.tens[n // 10] + "-" + self.units[n % 10]

    def _two_digit_to_french(self, n):
        """Helper method to convert numbers less than 100 to French."""
        if n < 10:
            return self.units[n]
        elif n < 17:
            return self.teens[n - 10]
        elif n < 20:
            return "dix-" + self.units[n - 10]

        # Belgian French variant handling for tens
        if self.lang == "be" and n < 100:
            return self._handle_tens(n)

        # Standard French rules
        if n < 70:
            return self._handle_tens(n)
        elif n in self.special_tens:
            return self.special_tens[n]
        elif n < 80:
            return "soixante-" + self._two_digit_to_french(n - 60)
        else:
            return "quatre-vingt" + (
                "s" if n == 80 else "-" + self._two_digit_to_french(n - 80)
            )

    def _three_digit_to_french(self, n):
        """Helper method to convert numbers less than 1000 to French."""
        if n < 100:
            return self._two_digit_to_french(n)
        elif n == 100:
            return "cent"
        else:
            hundreds = n // 100
            remainder = n % 100
            if hundreds == 1:
                return "cent" + (
                    ("-" + self._two_digit_to_french(remainder))
                    if remainder != 0
                    else ""
                )
            else:
                return (
                    self.units[hundreds]
                    + "-cent"
                    + (
                        ("-" + self._two_digit_to_french(remainder))
                        if remainder != 0
                        else "s"
                    )
                )

    def convert_number(self, n: int) -> str:
        """
        Converts a non-negative integer into its French word equivalent.
        
        Args:
            n (int): The number to convert (0 <= n <= 999,999).

        Returns:
            str: The French word equivalent of the number.

        Raises:
            ValueError: If the number is out of the supported range or is negative.
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError("Number must be a non-negative integer")
        if n >= 1000000:
            raise ValueError("Number out of supported range (must be less than 1,000,000)")

        if n < 1000:
            return self._three_digit_to_french(n)
        elif n < 2000:
            return "mille" + (
                ("-" + self._three_digit_to_french(n % 1000)) if n % 1000 != 0 else ""
            )
        else:
            thousands = n // 1000
            remainder = n % 1000
            return (
                self._three_digit_to_french(thousands)
                + "-mille"
                + (
                    ("-" + self._three_digit_to_french(remainder))
                    if remainder != 0
                    else "s"
                )
            )


def translate_to_french(number: int, lang: str = "fr") -> str:
    """
    Translates a non-negative integer into its French word equivalent using the specified language variant.
    
    Args:
        number (int): The number to convert.
        lang (str): The language variant for conversion ('fr' for French, 'be' for Belgian French).

    Returns:
        str: The French word equivalent of the number.

    Raises:
        ValueError: If the number is not a non-negative integer or out of the supported range.
    """
    if not isinstance(number, int) or number < 0:
        raise ValueError("Number must be a non-negative integer")
    return FrenchNumberTranslator(lang).convert_number(number)


def translate_to_french_list(list_of_numbers: list, lang: str = "fr", as_list: bool = False):
    """
    Translates a list of non-negative integers into their French word equivalents using the specified language variant.
    
    Args:
        list_of_numbers (list): A list of numbers to convert.
        lang (str): The language variant for conversion ('fr' for French, 'be' for Belgian French).
        as_list (bool): Whether to return the result as a list or a generator (default is False for a generator).

    Returns:
        generator or list: A generator or list of the French word equivalents of the numbers.

    Raises:
        ValueError: If the list is empty or contains invalid numbers.
    """
    if not list_of_numbers:
        raise ValueError("Can't process an empty list")

    result = (translate_to_french(number, lang) for number in list_of_numbers)
    return list(result) if as_list else result
