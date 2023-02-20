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
    _ = config.env.s3dir_artifacts
    _ = config.env.s3dir_data
    _ = config.env.workspace_signin_url

    _ = config.env.task_template_name
    _ = config.env.flow_definition_name
    _ = config.env.flow_definition_arn
    _ = config.env.flow_id

    _ = config.env.func_fullname_start_hil
    _ = config.env.func_fullname_post_process


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
