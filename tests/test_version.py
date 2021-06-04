import re


def try_parse_int(s, base=10, val=None):
    try:
        return int(s, base)
    except ValueError:
        return val


def test_version():
    """Test version string"""
    from coco2customvision import __version__

    version_parts = re.split("[.-]", __version__)
    if __version__ != "UNKNOWN":
        assert 3 <= len(version_parts), "must have at least Major.minor.patch"
        assert all(
            not try_parse_int(i) is None for i in version_parts[:2]
        ), f"Version Major.minor must be 2 integers. Received {__version__}"
