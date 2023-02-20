# -*- coding: utf-8 -*-

import pytest
import os
import json

from {{ cookiecutter.package_name }}.config.init import config


def test():
    # --------------------------------------------------------------------------
    # before
    # --------------------------------------------------------------------------
    s3path_reimbursement_request = config.env.s3dir_reimbursement_request.joinpath("request-1.json")
    s3path_reimbursement_request.write_text(json.dumps({
        "date_of_expense": "2020-01-01",
        "payment_method": "Credit Card",
        "purpose_of_expenditure": "Business Meal",
        "amount": "36.99",
    }))


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
