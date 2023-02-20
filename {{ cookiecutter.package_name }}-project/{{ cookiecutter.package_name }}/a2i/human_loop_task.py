# -*- coding: utf-8 -*-

"""
Single human loop task related.
"""

import dataclasses


@dataclasses.dataclass
class HumanLoopNameMaker:
    """
    Human Loop Name constructor. Human loop name has to be unique within an
    AWS region. My personal best practice for human loop name convention is
    ``${flow_id}-${task_id}-${uuid}``. Human loop name has a limit of
    maximum length of 63 characters. The total length of this naming convention
    has 6 + 1 + 40 + 1 + 12 = 60 characters.

    :param flow_id: Refers to the logical identifier of your human review workflow.
        It is typically composed of the first six characters of the hash value
        of the flow definition name. This identifier can be used to easily identify
        which human review workflow definition a particular task belongs to,
        without needing to call the ``describe_human_loop()`` API. flow_id
        cannot include hyphen.
    :param task_id: The human loop task requires a unique identifier of fewer
        than 40 characters. For instance, if each task relates to an S3 object,
        you could utilize the MD5 hash value of the S3 URI, which is typically
        32 characters long."
    :param uuid: For a given task, you may start multiple human loops. It is
        a randomly generated UUID with a maximum length of 12 characters.
        You can use ``uuid.uuid4().hex[:12]``. uuid cannot include hyphen.

    Ref:

    - https://docs.aws.amazon.com/augmented-ai/2019-11-07/APIReference/API_StartHumanLoop.html
    """

    flow_id: str = dataclasses.field()
    task_id: str = dataclasses.field()
    uuid: str = dataclasses.field()

    def __post_init__(self):
        if "-" in self.flow_id:
            raise ValueError("flow_id cannot include '-'!")
        if "-" in self.uuid:
            raise ValueError("uuid cannot include '-'!")

    @classmethod
    def from_human_loop_name(cls, human_loop_name: str) -> "HumanLoopNameMaker":
        parts = human_loop_name.split("-")
        flow_id = parts[0]
        task_id = "-".join(parts[1:-1])
        uuid = parts[-1]
        return cls(flow_id=flow_id, task_id=task_id, uuid=uuid)

    def to_human_loop_name(self) -> str:
        return f"{self.flow_id}-{self.task_id}-{self.uuid}"
