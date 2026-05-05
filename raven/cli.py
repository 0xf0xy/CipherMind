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

from raven.core import Raven
import argparse


def build_parser():
    parser = argparse.ArgumentParser(
        description="Raven: Command synthesis from intent",
        add_help=False,
    )

    synthesi = parser.add_argument_group("Synthesis")

    synthesi.add_argument(
        "input",
        nargs="+",
        help="Natural language description of the command you want to execute",
    )
    synthesi.add_argument(
        "-r",
        "--run",
        action="store_true",
        help="Run the synthesized command instead of just printing it",
    )

    meta = parser.add_argument_group("Information")
    meta.add_argument("-h", "--help", action="help", help="Show this help menu")
    meta.add_argument(
        "-v",
        "--version",
        action="version",
        version="Raven v1.0.0",
        help="Show program version",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    raven = Raven()
    user_input = " ".join(args.input)
    raven.synthesize(user_input, run=args.run)
