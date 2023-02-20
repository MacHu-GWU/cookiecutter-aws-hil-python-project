# -*- coding: utf-8 -*-

import os
import pytest

import aws_a2i
from {{ cookiecutter.package_name }}.paths import path_task_ui_template, path_task_ui_html

def test():
    input_data = {
        "date_of_expense": "2020-01-01",
        "payment_method": "Credit Card",
        "purpose_of_expenditure": "Business Meal",
        "amount": "36.99",
    }
    aws_a2i.render_task_template(
        task_template_content=path_task_ui_template.read_text(),
        input_data=input_data,
        path_task_ui_html=path_task_ui_html,
        preview=True,
    )


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
