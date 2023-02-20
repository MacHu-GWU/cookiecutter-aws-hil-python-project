# -*- coding: utf-8 -*-

import pytest
import os
import json

from {{ cookiecutter.package_name }}.logger import logger
from {{ cookiecutter.package_name }}.config.init import config


def _test():
    # --------------------------------------------------------------------------
    # before
    # --------------------------------------------------------------------------
    s3path_reimbursement_request = config.env.s3dir_reimbursement_request.joinpath(
        "request-1.json"
    )
    logger.info(f"preview s3path_reimbursement_request: {s3path_reimbursement_request.console_url}")
    s3path_reimbursement_request.write_text(
        json.dumps(
            {
                "date_of_expense": "2020-01-01",
                "payment_method": "Credit Card",
                "purpose_of_expenditure": "Business Meal",
                "amount": "36.99",
            }
        )
    )


def test():
    with logger.disabled(
        disable=True,
        # disable=False,
    ):
        _test()


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
