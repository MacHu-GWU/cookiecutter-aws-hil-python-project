# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from fixa.hashes import hashes, HashAlgoEnum

if T.TYPE_CHECKING:
    from .main import Env


@dataclasses.dataclass
class NameMixin:
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
    def dynamodb_table_name(self: "Env") -> str:
        """
        It shares the same dynamodb table from the ``aws_idp_doc_store`` project.
        """
        return f"{self.prefix_name_snake}-status_tracker"

    @property
    def flow_id(self: "Env") -> str:
        """
        All the doc type labeling human loop name in this environment will
        start with this prefix.
        """
        return hashes.of_str(
            self.prefix_name_snake,
            algo=HashAlgoEnum.sha256,
            hexdigest=True,
        )[:6]