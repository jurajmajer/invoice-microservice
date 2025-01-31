import logging
import os

log = logging.getLogger(__name__)


def read_env_var(env_name, log_error=True, default_value=None):
    ret_val = os.getenv(env_name)
    if log_error and ret_val is None:
        log.error('Environment variable %s is not set', env_name)
    if ret_val is None:
        ret_val = default_value
    return ret_val
