# -*- coding: utf-8 -*-

"""
AWS CloudFormation related automation script.

.. note::

    All of the deployment automation function should have a required parameter
    ``env_name``. We need to ensure developer explicitly know what env they
    are dealing with
"""

import os

import aws_a2i
from aws_codecommit import better_boto

from {{ cookiecutter.package_name }}.a2i.deploy import (
    deploy_human_review_workflow as _deploy_human_review_workflow,
    delete_human_review_workflow as _delete_human_review_workflow,
)
from {{ cookiecutter.package_name }}.boto_ses import bsm
from {{ cookiecutter.package_name }}.config.init import config

from .git import (
    GIT_BRANCH_NAME,
    IS_HIL_BRANCH,
    IS_INT_BRANCH,
    IS_RELEASE_BRANCH,
    IS_CLEAN_UP_BRANCH,
    COMMIT_MESSAGE_HAS_HIL,
)
from .runtime import IS_CI
from .logger import logger
from .emoji import Emoji
from .env import CURRENT_ENV
from .hil_rule import (
    do_we_deploy_hil,
    do_we_delete_hil,
)


@logger.block(
    msg="Deploy Human Review Workflow",
    start_emoji=f"{Emoji.deploy} {Emoji.technologist}",
    end_emoji=f"{Emoji.deploy} {Emoji.technologist}",
    pipe=Emoji.technologist,
)
def deploy_human_review_workflow(
    env_name: str = CURRENT_ENV,
    check: bool = True,
):
    try:
        if check:
            if (
                do_we_deploy_hil(
                    env_name=env_name,
                    is_ci_runtime=IS_CI,
                    branch_name=GIT_BRANCH_NAME,
                    is_hil_branch=IS_HIL_BRANCH,
                    is_int_branch=IS_INT_BRANCH,
                    is_release_branch=IS_RELEASE_BRANCH,
                )
                is False
            ):
                return
        _deploy_human_review_workflow(env_name)
        logger.info(f"{Emoji.succeeded} Deploy Human Review Workflow succeeded!")
        # in CI, post the Human Review Workflow url to the PR comment if possible
        if IS_CI:
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                flow_def_console_url = aws_a2i.get_flow_definition_console_url(
                    aws_region=bsm.aws_region,
                    flow_definition_name=config.get_env(env_name).flow_definition_name,
                )
                content = "\n".join(
                    [
                        f"{Emoji.succeeded} {Emoji.technologist}️ **Deploy Human Review Workflow succeeded**",
                        f"",
                        f"- review [Human Review Workflow]({flow_def_console_url})",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
    except Exception as e:
        logger.error(f"{Emoji.failed} Deploy Human Review Workflow failed!")
        # in CI, post the error message to the PR comment if possible
        if IS_CI:
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                content = "\n".join(
                    [
                        f"{Emoji.failed} {Emoji.technologist}️ Deploy Human Review Workflow failed!",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
        raise e


@logger.block(
    msg="Delete Human Review Workflow",
    start_emoji=f"{Emoji.delete} {Emoji.technologist}",
    end_emoji=f"{Emoji.delete} {Emoji.technologist}",
    pipe=Emoji.technologist,
)
def delete_human_review_workflow(
    env_name: str = CURRENT_ENV,
    check: bool = True,
):
    try:
        if check:
            if (
                do_we_delete_hil(
                    env_name=env_name,
                    is_ci_runtime=IS_CI,
                    is_clean_up_branch=IS_CLEAN_UP_BRANCH,
                    commit_message_has_hil=COMMIT_MESSAGE_HAS_HIL,
                )
                is False
            ):
                return
        _delete_human_review_workflow(env_name)
        logger.info(f"{Emoji.succeeded} Delete Human Review Workflow succeeded!")
        if IS_CI:
            # post reply to codecommit PR thread, if possible
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                flow_def_console_url = aws_a2i.get_flow_definition_console_url(
                    aws_region=bsm.aws_region,
                    flow_definition_name=config.get_env(env_name).flow_definition_name,
                )
                content = "\n".join(
                    [
                        f"{Emoji.succeeded} {Emoji.technologist}️ **Delete Human Review Workflow succeeded**",
                        f"",
                        f"- review [Human Review Workflow]({flow_def_console_url})",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
    except Exception as e:
        logger.error(f"{Emoji.failed} Delete Human Review Workflow failed!")
        if IS_CI:
            # post reply to codecommit PR thread, if possible
            comment_id = os.environ.get("CI_DATA_COMMENT_ID", "")
            if comment_id:
                content = "\n".join(
                    [
                        f"{Emoji.failed} Delete Human Review Workflow failed!",
                    ]
                )
                better_boto.post_comment_reply(
                    bsm=bsm,
                    in_reply_to=comment_id,
                    content=content,
                )
        raise e
