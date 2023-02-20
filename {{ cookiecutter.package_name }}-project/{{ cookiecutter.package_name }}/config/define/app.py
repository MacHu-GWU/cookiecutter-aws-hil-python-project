# -*- coding: utf-8 -*-

import typing as T
import dataclasses

import aws_a2i
from s3pathlib import S3Path

from ...compat import cached_property
from ...boto_ses import bsm


if T.TYPE_CHECKING:
    from .main import Env


@dataclasses.dataclass
class AppMixin:
    s3uri_data: T.Optional[str] = dataclasses.field(default=None)
    private_team_arn: T.Optional[str] = dataclasses.field(default=None)
    use_dynamodb_tracker: T.Optional[bool] = dataclasses.field(default=False)

    @property
    def s3dir_data(self: "Env") -> S3Path:
        return S3Path.from_s3_uri(self.s3uri_data).to_dir()

    @property
    def s3dir_reimbursement_request(self: "Env") -> S3Path:
        """
        Where you store the reimbursement request documents.
        """
        return self.s3dir_data.joinpath("01-reimbursement-request").to_dir()

    @property
    def s3dir_hil_output(self: "Env") -> S3Path:
        """
        Where you store the output of the HIL process.
        """
        return self.s3dir_data.joinpath("02-hil-output").to_dir()

    @cached_property
    def workspace_signin_url(self: "Env") -> str:
        work_team_name = aws_a2i.parse_team_name_from_private_team_arn(self.private_team_arn)
        return aws_a2i.get_workspace_signin_url(bsm, work_team_name)
