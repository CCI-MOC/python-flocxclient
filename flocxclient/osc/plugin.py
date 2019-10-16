import logging

from osc_lib import utils


DEFAULT_API_VERSION = '1'

# Required by the OSC plugin interface
API_NAME = 'market'
API_VERSION_OPTION = 'os_market_api_version'
API_VERSIONS = {
    '1': 'flocxclient.v1.client.Client',
}

OS_MARKET_API_LATEST = True
LATEST_VERSION = 1.


LOG = logging.getLogger(__name__)

# Required by the OSC plugin interface


def make_client(instance):
    """Returns a client to the ClientManager

    Called to instantiate the requested client version.  instance has
    any available auth info that may be required to prepare the client.

    :param ClientManager instance: The ClientManager that owns the new client
    """

    requested_api_version = instance._api_version[API_NAME]

    plugin_client = utils.get_client_class(
        API_NAME,
        requested_api_version,
        API_VERSIONS)

    client = plugin_client(
        os_flocx_api_version=requested_api_version,
        # enable re-negotiation of the latest version, if CLI
        # latest is too high for the server we're talking to.
        session=instance.session,
        region_name=instance._region_name,
        endpoint_override=None
        )

    return client


# Required by the OSC plugin interface
def build_option_parser(parser):

    """Hook to add global options

    Called from openstackclient.shell.OpenStackShell.__init__()
    after the builtin parser has been initialized.  This is
    where a plugin can add global options such as an API version setting.

    :param argparse.ArgumentParser parser: The parser object that has been
        initialized by OpenStackShell.
    """
    parser.add_argument(
        '--os-market-api-version',
        metavar='<market-api-version>',
        help='market API version, default=' +
             DEFAULT_API_VERSION +
             ' (Env: OS_MARKET_API_VERSION)')

    return parser
