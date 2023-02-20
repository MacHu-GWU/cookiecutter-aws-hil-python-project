# -*- coding: utf-8 -*-

import typing as T
import dataclasses

if T.TYPE_CHECKING:
    from .main import Env


@dataclasses.dataclass
class NameMixin:
    """
    This mixin class derive all AWS Resource name based on the project name
    and the env name.
    """
    pass
