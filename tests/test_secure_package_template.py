import re

import secure_package_template


def test_version() -> None:
    assert isinstance(secure_package_template.__version__, str)
    assert re.match(r"^[0-9][0-9\.]*[0-9]$", secure_package_template.__version__)
