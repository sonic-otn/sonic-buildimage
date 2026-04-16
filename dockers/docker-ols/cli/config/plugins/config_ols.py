import click
from swsscommon.swsscommon import ConfigDBConnector

import utilities_common.cli as clicommon


# ---------------------------------------------------------------------------
# Top-level 'ols' group
# ---------------------------------------------------------------------------

@click.group(cls=clicommon.AliasedGroup, name="ols")
def ols():
    """OLS (Optical Line System) configuration."""
    pass

# ---------------------------------------------------------------------------
# Plugin registration
# ---------------------------------------------------------------------------

def register(cli):
    cli.add_command(ols)


if __name__ == '__main__':
    ols()
