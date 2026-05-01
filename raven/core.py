"""
MIT License

Copyright (c) 2026 0xf0xy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import subprocess
import json
import re
import os

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
RESET = "\033[0m"

IPV4 = (
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}"
)
DOMAIN = r"(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"
HOST = r"[a-zA-Z0-9.-]+"
TARGET = rf"({IPV4}|{DOMAIN}|{HOST})"


class Raven:
    """
    Raven: Command synthesis from intent.
    """

    def __init__(self):
        """
        Initialize the Raven command synthesizer by loading command templates from a JSON file.
        """
        with open("raven/data/templates.json", "r") as f:
            templates = json.load(f)

        self.patterns = templates

    @staticmethod
    def _keywords_match(keywords: list[str], text: str) -> bool:
        """
        Check if any of the keywords are present in the text.

        Args:
            keywords (list[str]): A list of keywords to check for
            text (str): The input text to check

        Returns:
            bool: True if any keyword is found in the text, False otherwise
        """
        text = text.lower()

        return any(keyword in text for keyword in keywords)

    def get_command(self, intent: str, user_input: str) -> str | None:
        """
        Get the command template for the given intent and user input.

        Args:
            intent (str): The predicted intent label
            user_input (str): The original user input text

        Returns:
            str or None: The generated command if a matching pattern is found, None otherwise
        """
        if intent not in self.patterns:
            return None

        user_input = user_input.strip()

        for pattern in self.patterns[intent]:

            if not self._keywords_match(pattern["keywords"], user_input):
                continue

            regex_pattern = pattern["regex"].format(TARGET=TARGET)

            match = re.search(regex_pattern, user_input, re.IGNORECASE)

            if not match:
                continue

            args = match.groups()

            try:
                if args:
                    return pattern["template"].format(*args)

                else:
                    return pattern["template"]

            except IndexError:
                return None

        return None

    def synthesize(self, user_input: str, run: bool = False) -> None:
        """
        Synthesize a command from user input by trying all available intents.

        Args:
            user_input (str): The user's natural language input
            run (bool): Whether to execute the command after synthesis (default: False)

        Returns:
            None: This method does not return a value, it either prints the synthesized command or executes it.
        """
        os.system("clear")

        for intent in self.patterns:
            command = self.get_command(intent, user_input)

            if command:
                if run:
                    print(f"Executing → {GREEN}{command}{RESET}")
                    print("─" * 50 + "\n")

                    try:
                        result = subprocess.run(command, shell=True)

                        if result.returncode != 0:
                            print(
                                f"\n[{RED}x{RESET}] Command failed with exit code {result.returncode}"
                            )

                    except Exception as e:
                        print(f"[{RED}x{RESET}] Failed to execute: {e}")

                else:
                    print(f"Synthesized command → {GREEN}{command}{RESET}")

                return

        print(f"[{RED}x{RESET}] No matching command found for: {user_input}")
