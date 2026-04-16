import click
from natsort import natsorted
from tabulate import tabulate
from swsscommon.swsscommon import ConfigDBConnector, SonicV2Connector

import utilities_common.cli as clicommon

# ===========================================================================
# Top-level 'ols' group
# ===========================================================================

@click.group(cls=clicommon.AliasedGroup, name="ols")
def ols():
    """Show OLS (Optical Line System) information."""
    pass



# ---------------------------------------------------------------------------
# Plugin registration
# ---------------------------------------------------------------------------

def register(cli):
    cli.add_command(ols)


if __name__ == '__main__':
    ols()
