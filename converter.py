class FrenchNumberTranslator:
    """
    A class to convert non-negative integers into their French word equivalents.
    Supports numbers from 0 to 999,999.
    """

    def __init__(self, lang: str = "fr") -> None:
        self.lang = lang

        # Base number mappings
        self.units = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"]
        self.teens = ["dix", "onze", "douze", "treize", "quatorze", "quinze", "seize"]

        # Define the language-specific tens and special tens
        if self.lang == "fr":
            self.tens = ["", "dix", "vingt", "trente", "quarante", "cinquante", "soixante"]
            self.special_tens = {70: "soixante-dix", 71: "soixante-et-onze", 80: "quatre-vingts", 90: "quatre-vingt-dix"}
        elif self.lang == "be":
            self.tens = ["", "dix", "vingt", "trente", "quarante", "cinquante", "soixante", "septante", "huitante", "nonante"]
        else:
            raise ValueError(f"Unsupported language variant: {lang}. Supported variants are 'fr' and 'be'.")

    def _handle_tens(self, n: int) -> str:
        """Helper method to handle tens and units."""
        if n % 10 == 0:
            return self.tens[n // 10]
        if n % 10 == 1 and n != 11:
            return self.tens[n // 10] + "-et-un"
        return self.tens[n // 10] + "-" + self.units[n % 10]

    def _two_digit_to_french(self, n: int) -> str:
        """Convert two-digit numbers to French."""
        if n < 10:
            return self.units[n]
        if n < 17:
            return self.teens[n - 10]
        if n < 20:
            return "dix-" + self.units[n - 10]

        if self.lang == "be" and n < 100:
            return self._handle_tens(n)

        if n < 70:
            return self._handle_tens(n)
        if n in self.special_tens:
            return self.special_tens[n]
        if n < 80:
            return "soixante-" + self._two_digit_to_french(n - 60)
        return "quatre-vingt" + ("s" if n == 80 else "-" + self._two_digit_to_french(n - 80))

    def _three_digit_to_french(self, n: int) -> str:
        """Convert three-digit numbers to French."""
        if n < 100:
            return self._two_digit_to_french(n)
        if n == 100:
            return "cent"
        
        hundreds = n // 100
        remainder = n % 100
        if hundreds == 1:
            return "cent" + ("-" + self._two_digit_to_french(remainder) if remainder != 0 else "")
        return self.units[hundreds] + "-cent" + ("-" + self._two_digit_to_french(remainder) if remainder != 0 else "s")

    def convert_number(self, n: int) -> str:
        """Convert a non-negative integer to French."""
        if not isinstance(n, int) or n < 0:
            raise ValueError("Number must be a non-negative integer")
        if n >= 1000000:
            raise ValueError("Number out of supported range (must be less than 1,000,000)")

        if n < 1000:
            return self._three_digit_to_french(n)
        if n < 2000:
            return "mille" + ("-" + self._three_digit_to_french(n % 1000) if n % 1000 != 0 else "")
        
        thousands = n // 1000
        remainder = n % 1000
        return self._three_digit_to_french(thousands) + "-mille" + ("-" + self._three_digit_to_french(remainder) if remainder != 0 else "s")


def translate_to_french(number: int, lang: str = "fr") -> str:
    """Helper function to translate a number to French."""
    translator = FrenchNumberTranslator(lang)
    return translator.convert_number(number)


def translate_to_french_list(list_of_numbers: list, lang: str = "fr", as_list: bool = False):
    """Translates a list of numbers to French words."""
    if not list_of_numbers:
        raise ValueError("Can't process an empty list")

    translator = FrenchNumberTranslator(lang)
    result = (translator.convert_number(number) for number in list_of_numbers)
    
    return list(result) if as_list else result
