"""
Show CLI platform filter plugin.

Filename starts with zzz_ to ensure this plugin loads LAST,
after all other plugins have registered their commands.
"""


def register(cli):
    from sonic_cli_filter import filter_commands
    filter_commands("show", cli)
