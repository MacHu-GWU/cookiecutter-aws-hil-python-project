# -*- coding: utf-8 -*-

import os
import pytest
from {{ cookiecutter.package_name }}.config.init import config


def test():
    # constant
    _ = config

    _ = config.env

    # constant attributes
    _ = config.env.s3uri_artifacts
    _ = config.env.s3uri_data
    _ = config.env.private_team_arn

    # derived attributes


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
