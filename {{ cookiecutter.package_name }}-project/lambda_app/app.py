# -*- coding: utf-8 -*-

from chalice import Chalice
from chalice.app import S3Event

from {{ cookiecutter.package_name }}.config.init import config
from {{ cookiecutter.package_name }}.iac.output import Output
from {{ cookiecutter.package_name }}.lbd.handlers import start_hil, post_process

env = config.env
app = Chalice(app_name=env.chalice_app_name)

stack_output = Output.get()


@app.on_s3_event(
    name=env.func_fullname_start_hil,
    bucket=env.s3dir_reimbursement_request.bucket,
    prefix=env.s3dir_reimbursement_request.key,
)
def start_hil_lambda_handler(event: S3Event):
    return start_hil(event.bucket, event.key)



@app.on_s3_event(
    name=env.func_fullname_post_process,
    bucket=env.s3dir_hil_output.bucket,
    prefix=env.s3dir_hil_output.key,
)
def post_process_handler(event: S3Event):
    return post_process(event.bucket, event.key)
