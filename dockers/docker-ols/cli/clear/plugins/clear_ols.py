import click
from natsort import natsorted
from swsscommon.swsscommon import ConfigDBConnector, SonicV2Connector

import utilities_common.cli as clicommon

# ---------------------------------------------------------------------------
# Top-level 'ols' group
# ---------------------------------------------------------------------------

@click.group(cls=clicommon.AliasedGroup, name="ols")
def ols():
    """Clear OLS (Optical Line System) entries."""
    pass


# ---------------------------------------------------------------------------
# Plugin registration
# ---------------------------------------------------------------------------

def register(cli):
    cli.add_command(ols)


if __name__ == '__main__':
    ols()
