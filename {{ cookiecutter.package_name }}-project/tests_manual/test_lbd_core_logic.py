# -*- coding: utf-8 -*-

import json
import aws_a2i
from s3pathlib import S3Path

from {{ cookiecutter.package_name }}.config.init import config
from {{ cookiecutter.package_name }}.boto_ses import bsm
from {{ cookiecutter.package_name }}.lbd.core_logic import start_hil, post_process_hil_output


def test():
    # --------------------------------------------------------------------------
    # before
    # --------------------------------------------------------------------------
    reimbursement_request_data = {
        "date_of_expense": "2020-01-01",
        "payment_method": "Credit Card",
        "purpose_of_expenditure": "Business Meal",
        "amount": "36.99",
    }
    s3path_reimbursement_request = config.env.s3dir_data.joinpath(
        "manual-test",
        "sample_reimbursement_request.json",
    )
    s3path_reimbursement_request.write_text(json.dumps(reimbursement_request_data))

    # --------------------------------------------------------------------------
    # invoke
    # --------------------------------------------------------------------------
    human_loop_arn = start_hil(s3path_reimbursement_request)

    input("Finish human loop task first, then Press any key to continue: ")
    response = aws_a2i.describe_human_loop(
        bsm=bsm, human_loop_name=human_loop_arn.split("/")[-1]
    )
    s3uri_hil_output = response["HumanLoopOutput"]["OutputS3Uri"]
    post_process_hil_output(S3Path.from_s3_uri(s3uri_hil_output))


if __name__ == "__main__":
    from {{ cookiecutter.package_name }}.tests import run_cov_test

    run_cov_test(__file__, "{{ cookiecutter.package_name }}.lbd.core_logic", preview=False)
