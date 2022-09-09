from unittest.mock import MagicMock

import pytest

from conan.api.conan_api import ConanAPIV2
from conan.tools.files import save
from conan.cli.common import get_profiles_from_args
from conans.client.cache.cache import ClientCache
from conans.errors import ConanException
from conans.test.utils.test_files import temp_folder


@pytest.fixture()
def conan_api():
    tmp_folder = temp_folder()
    cache = ClientCache(tmp_folder)
    save(None, cache.default_profile_path, "")
    return ConanAPIV2(tmp_folder)


@pytest.fixture()
def argparse_args():
    return MagicMock(
        profile_build=None,
        profile_host=None,
        settings_build=None,
        settings_host=None,
        options_build=None,
        options_host=None,
        conf_build=None,
        conf_host=None
    )


@pytest.mark.parametrize("conf_name", [
    "core.doesnotexist:never",
    "core:doesnotexist"
])
def test_core_confs_not_allowed_via_cli(conan_api, argparse_args, conf_name):
    argparse_args.conf_build = [conf_name]
    argparse_args.conf_host = [conf_name]

    with pytest.raises(ConanException) as exc:
        get_profiles_from_args(conan_api, argparse_args)
    assert "[conf] 'core.*' configurations are not allowed in profiles" in str(exc.value)