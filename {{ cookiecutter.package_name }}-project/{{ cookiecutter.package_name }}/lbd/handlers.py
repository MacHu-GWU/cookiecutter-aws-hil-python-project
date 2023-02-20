# -*- coding: utf-8 -*-

from s3pathlib import S3Path
from . import core_logic


def start_hil(bucket: str, key: str) -> dict:
    human_loop_arn = core_logic.start_hil(s3path_reimbursement_request=S3Path(bucket, key))
    return {
        "human_loop_arn": human_loop_arn
    }

def post_process(bucket: str, key: str) -> dict:
    decision = core_logic.post_process_hil_output(s3path_hil_output=S3Path(bucket, key))
    return {
        "decision": decision
    }
