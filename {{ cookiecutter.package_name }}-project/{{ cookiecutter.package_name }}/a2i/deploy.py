# -*- coding: utf-8 -*-

"""
Amazon Augmented AI deployment automation, deploy and delete:

- Task UI template
- Human review workflow definition
"""

import aws_a2i

from .._version import __version__
from ..paths import path_task_ui_template
from ..config.define import Env
from ..config.init import config
from ..boto_ses import bsm
from ..iac.output import Output


def deploy_human_review_workflow(
    env_name: str,
):
    env: Env = config.get_env(env_name)

    tags = dict(
        ProjectName=env.project_name,
        EnvName=env.env_name,
        PackageVersion=__version__,
    )

    # deploy hil task template
    aws_a2i.deploy_hil_task_template(
        bsm=bsm,
        task_template_name=env.task_template_name,
        task_template_content=path_task_ui_template.read_text(),
        tags=tags,
    )

    # get ``iam_role_human_review_workflow_arn`` for cloudformation stack output
    output = Output.get(env_name)

    # deploy flow definition
    aws_a2i.deploy_flow_definition(
        bsm=bsm,
        flow_definition_name=env.flow_definition_name,
        flow_execution_role_arn=output.iam_role_human_review_workflow_arn,
        labeling_team_arn=env.private_team_arn,
        output_bucket=env.s3dir_hil_output.bucket,
        output_key=env.s3dir_hil_output.key,
        task_template_name=env.task_template_name,
        task_description="Example human review workflow",
        task_count=1,
        task_availability_life_time_in_seconds=24 * 60 * 60,
        task_time_limit_in_seconds=60 * 60,
        tags=tags,
    )


def delete_human_review_workflow(
    env_name: str,
):
    env: Env = config.get_env(env_name)

    aws_a2i.remove_flow_definition(
        bsm=bsm,
        flow_definition_name=env.flow_definition_name,
        wait=False,
    )

    aws_a2i.remove_hil_task_template(
        bsm=bsm,
        task_template_name=env.task_template_name,
    )
