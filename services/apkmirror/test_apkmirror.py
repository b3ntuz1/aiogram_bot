from services.apkmirror import apkmirror
import re
import pytest


@pytest.fixture()
def apk():
    return apkmirror.ApkMirror("niantic-inc/pokemon-go")
# @pytest.fixture()
# def apk():
#     return apkmirror.ApkMirror("the-pokemon-company/pokemon-home")


def test_success(apk):
    result = apk.parse()
    assert result is True


def test_return_types(apk):
    apk.parse()
    assert type(apk.link()) == str
    assert type(apk.version()) == str
    assert type(apk.whats_new()) == str
    assert type(apk.description()) == str


def test_link(apk):
    apk.parse()
    string = apk.link()
    r = re.compile(r"\/[\w-]+?\/.*?\d+.*?[-]release")
    result = r.findall(string)
    assert len(result) == 1


def test_version(apk):
    apk.parse()
    string = apk.version()
    ver = re.compile(r"\d\.\d{1,3}\.\d")
    assert len(ver.findall(string)) == 1


def test_app_title(apk):
    apk.parse()
    app_title = apk.app_title()
    assert app_title == "Pokémon GO"
