import argparse
import logging
import re
import random
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataContextualReplacer:
    """
    Replaces data based on contextual keywords identified nearby.
    """

    def __init__(self, keywords, window_size=10, replacement_value=None, faker_locale='en_US'):
        """
        Initializes the DataContextualReplacer.

        Args:
            keywords (list): A list of contextual keywords.
            window_size (int): The number of words to check around the target. Defaults to 10.
            replacement_value (str, optional): The value to replace matched data with. If None, a random float is generated using Faker. Defaults to None.
            faker_locale (str, optional): The Faker locale to use for generating replacement values. Defaults to 'en_US'.
        """
        if not isinstance(keywords, list):
            raise TypeError("Keywords must be a list.")
        if not all(isinstance(keyword, str) for keyword in keywords):
            raise TypeError("All keywords must be strings.")
        if not isinstance(window_size, int) or window_size <= 0:
            raise ValueError("Window size must be a positive integer.")

        self.keywords = keywords
        self.window_size = window_size
        self.replacement_value = replacement_value
        self.fake = Faker(faker_locale)  # Moved Faker instantiation here

    def replace_data(self, text):
        """
        Replaces data based on contextual keywords.

        Args:
            text (str): The input text.

        Returns:
            str: The text with masked data.
        """
        try:
            if not isinstance(text, str):
                raise TypeError("Input must be a string.")

            words = text.split()
            new_words = []
            for i, word in enumerate(words):
                if self._is_number(word):
                    # Check for keywords within the window
                    start = max(0, i - self.window_size)
                    end = min(len(words), i + self.window_size + 1)
                    context = words[start:i] + words[i + 1:end] # Exclude current word

                    if any(keyword in ' '.join(context).lower() for keyword in self.keywords):
                        logging.debug(f"Found keyword near '{word}'. Masking...")
                        if self.replacement_value is not None:
                            replacement = self.replacement_value
                        else:
                            replacement = str(round(random.uniform(10000, 1000000), 2)) # Example range, configurable
                        new_words.append(replacement)
                    else:
                        new_words.append(word)
                else:
                    new_words.append(word)

            return ' '.join(new_words)

        except Exception as e:
            logging.error(f"Error processing text: {e}")
            raise

    def _is_number(self, string):
       """
       Checks if a string is a number (int or float).

       Args:
           string (str): The string to check.

       Returns:
           bool: True if the string is a number, False otherwise.
       """
       try:
           float(string)
           return True
       except ValueError:
           return False


def setup_argparse():
    """
    Sets up the argument parser.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Replaces data based on contextual keywords.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="The input text to process."
    )
    parser.add_argument(
        "--keywords",
        type=str,
        required=True,
        help="Comma-separated list of contextual keywords."
    )
    parser.add_argument(
        "--window_size",
        type=int,
        default=10,
        help="The number of words to check around the target (default: 10)."
    )
    parser.add_argument(
        "--replacement_value",
        type=str,
        default=None,
        help="The value to replace matched data with. If not provided, a random float is generated."
    )
    parser.add_argument(
        "--faker_locale",
        type=str,
        default="en_US",
        help="The Faker locale to use for generating replacement values (default: en_US)."
    )
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)."
    )

    return parser


def main():
    """
    Main function to execute the data contextual replacer.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # Configure logging level based on command-line argument
    logging.getLogger().setLevel(args.log_level)


    try:
        keywords = [keyword.strip() for keyword in args.keywords.split(",")]
        replacer = DataContextualReplacer(
            keywords=keywords,
            window_size=args.window_size,
            replacement_value=args.replacement_value,
            faker_locale=args.faker_locale
        )
        masked_text = replacer.replace_data(args.input)
        print(masked_text)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    main()

# Usage examples (can be placed in a separate documentation file or help section)
#
# Example 1: Basic usage with keywords and default window size
# python main.py --input "My salary is 50000 and bonus is 1000" --keywords "salary,income"
#
# Example 2: Specifying window size
# python main.py --input "Income: 60000, expenses: 2000" --keywords "income,salary" --window_size 5
#
# Example 3: Providing a replacement value
# python main.py --input "The CEO earns 2000000" --keywords "salary,earn" --replacement_value "REDACTED"
#
# Example 4: Using a different Faker locale
# python main.py --input "Le salaire est 75000 euros" --keywords "salaire,revenu" --faker_locale "fr_FR"
#
# Example 5: Setting the log level to DEBUG
# python main.py --input "My income is 70000" --keywords "income" --log_level DEBUG