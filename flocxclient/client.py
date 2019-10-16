import logging

from keystoneauth1 import loading as kaloading

from oslo_utils import importutils


LOG = logging.getLogger(__name__)


def get_client(api_version, auth_type=None, os_flocx_api_version=None,
               max_retries=None, retry_interval=None, **kwargs):

    """Get an authenticated client, based on the credentials.
    :param api_version: the API version to use. Valid value: '1'.
    :param auth_type: type of keystoneauth auth plugin loader to use.
    :param os_flocx_api_version: ironic API version to use.
    :param max_retries: Maximum number of retries in case of conflict error
    :param retry_interval: Amount of time (in seconds) between retries in case
        of conflict error.
    :param kwargs: all the other params that are passed to keystoneauth.
    """

    if auth_type is None:
        if 'endpoint' in kwargs:
            if 'token' in kwargs:
                auth_type = 'admin_token'
            else:
                auth_type = 'none'
        elif 'token' in kwargs and 'auth_url' in kwargs:
            auth_type = 'token'
        else:
            auth_type = 'password'
    session = kwargs.get('session')
    if not session:
        loader = kaloading.get_plugin_loader(auth_type)
        loader_options = loader.get_options()
        # option.name looks like 'project-name', while dest will be the actual
        # argument name to which the value will be passed to (project_name)
        auth_options = [o.dest for o in loader_options]
        # Include deprecated names as well
        auth_options.extend([d.dest for o in loader_options
                             for d in o.deprecated])
        auth_kwargs = {k: v for (k, v) in kwargs.items() if k in auth_options}
        auth_plugin = loader.load_from_options(**auth_kwargs)
        # Let keystoneauth do the necessary parameter conversions
        session_loader = kaloading.session.Session()
        session_opts = {k: v for (k, v) in kwargs.items() if k in
                        [o.dest for o in session_loader.get_conf_options()]}
        session = session_loader.load_from_options(auth=auth_plugin,
                                                   **session_opts)

    # Make sure we also pass the endpoint interface to the HTTP client.
    # NOTE(gyee/efried): 'interface' in ksa config is deprecated in favor of
    # 'valid_interfaces'. So, since the caller may be deriving kwargs from
    # conf, accept 'valid_interfaces' first. But keep support for 'interface',
    # in case the caller is deriving kwargs from, say, an existing Adapter.
    interface = kwargs.get('valid_interfaces', kwargs.get('interface'))

    endpoint = kwargs.get('endpoint')
    if not endpoint:
        try:
            # endpoint will be used to get hostname
            # and port that will be used for API version caching.
            # NOTE(gyee): KSA defaults interface to 'public' if it is
            # empty or None so there's no need to set it to publicURL
            # explicitly.
            endpoint = session.get_endpoint(
                service_type=kwargs.get('service_type') or 'flocx',
                interface=interface,
                region_name=kwargs.get('region_name')
            )
        except Exception:
            # placeholder for actual error handling
            raise Exception

    flocxclient_kwargs = {
        'os_market_api_version': os_flocx_api_version,
        'max_retries': max_retries,
        'retry_interval': retry_interval,
        'session': session,
        'endpoint_override': endpoint,
        'interface': interface
    }

    return Client(api_version, **flocxclient_kwargs)


def Client(version, *args, **kwargs):

    module = importutils.import_versioned_module('flocxclient',
                                                 version, 'client')
    client_class = getattr(module, 'Client')
    return client_class(*args, **kwargs)
