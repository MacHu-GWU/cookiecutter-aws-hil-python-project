# -*- coding: utf-8 -*-

import typing as T
import dataclasses

import aws_a2i
from fixa.hashes import hashes, HashAlgoEnum

from ...boto_ses import bsm

if T.TYPE_CHECKING:
    from .main import Env


@dataclasses.dataclass
class A2IMixin:
    """
    This mixin class derive all AWS Resource name based on the project name
    and the env name.
    """
    @property
    def task_template_name(self: "Env") -> str:
        return self.prefix_name_slug

    @property
    def flow_definition_name(self: "Env") -> str:
        return self.prefix_name_slug

    @property
    def flow_definition_arn(self: "Env") -> str:
        return aws_a2i.get_flow_definition_arn(
            aws_account_id=bsm.aws_account_id,
            aws_region=bsm.aws_region,
            flow_definition_name=self.flow_definition_name,
        )

    @property
    def flow_id(self: "Env") -> str:
        return hashes.of_str(
            self.prefix_name_snake,
            algo=HashAlgoEnum.sha256,
            hexdigest=True,
        )[:6]