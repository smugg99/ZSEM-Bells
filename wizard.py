#!/usr/bin/env python3

import click
from tabulate import tabulate
from typing import Dict

from classes.user_config_manager import UserConfigManager
from data.lang_bindings import LangBindingsManager

user_config_manager = UserConfigManager()
user_config: Dict[str, any] = user_config_manager.get_config()

bindings_manager = LangBindingsManager()
bindings_manager.load_bindings(user_config["lang_path"])
bindings: Dict[str, any] = bindings_manager.get_bindings()


def main():
    click.echo(bindings["wizard"]["greeting"])
    click.echo(bindings["wizard"]["description"])


if __name__ == "__main__":
    main()
