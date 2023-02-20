# -*- coding: utf-8 -*-

import typing as T
import json
import uuid
import random

import aws_a2i
from s3pathlib import S3Path
from fixa.hashes import HashAlgoEnum, hashes

from ..config.init import config
from ..boto_ses import bsm
from ..logger import logger
from ..emoji import Emoji
from ..a2i.human_loop_task import (
    HumanLoopNameMaker,
)


@logger.block(
    msg="Start Human Loop Task",
    pipe=Emoji.eye,
)
def start_hil(s3path_reimbursement_request: S3Path) -> T.Optional[str]:
    if random.randint(1, 100) <= 100:
        logger.info(f"Sign in to workspace: {config.env.workspace_signin_url}")
        human_loop_name = HumanLoopNameMaker(
            flow_id=config.env.flow_id,
            task_id=hashes.of_str(
                s3path_reimbursement_request.uri,
                algo=HashAlgoEnum.md5,
            ),
            uuid=uuid.uuid4().hex[:12],
        ).to_human_loop_name()
        logger.info(f"▶️ Start a Human Loop Task {human_loop_name!r}")
        hil_console_url = aws_a2i.get_hil_console_url(
            bsm.aws_region, config.env.flow_definition_name, human_loop_name
        )
        logger.info(f"You can preview HIL status at {hil_console_url}", indent=1)
        human_loop_arn = aws_a2i.start_human_loop(
            bsm=bsm,
            human_loop_name=human_loop_name,
            flow_definition_arn=config.env.flow_definition_arn,
            input_data=json.loads(s3path_reimbursement_request.read_text()),
            verbose=False,
        )
        return human_loop_arn


@logger.block(
    msg="Post Process HIL Output",
    pipe=Emoji.eye,
)
def post_process_hil_output(s3path_hil_output: S3Path) -> T.Optional[str]:
    hil_output_data = json.loads(s3path_hil_output.read_text())
    answers: T.List[bool] = list()
    for human_answer in hil_output_data["humanAnswers"]:
        answers.append(human_answer["answerContent"]["decision"]["approve"])
    if sum(answers) in [0, len(answers)]:
        # all reviewers give the same answer:
        is_approve = answers[0]
        if is_approve:
            decision = "Approve"
        else:
            decision = "Deny"
        logger.info(
            f"{Emoji.succeeded} all reviewers gives the same decision '{decision}'."
        )
        # do something
        return decision
    else:
        logger.info(
            f"{Emoji.failed} reviewers give different decisions, final decision is unknown."
        )
        return "Unknown"
