# -*- coding: utf-8 -*-

import typing as T
import attr
import cottonformation as cf
from cottonformation.res import iam

if T.TYPE_CHECKING:
    from .main import Stack


@attr.s
class IamMixin:
    def mk_rg1_iam(self: "Stack"):
        """
        It is very common to declare a group of IAM resources for the project.

        Ref:

        - IAM Object quotas: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entities
        """
        # declare a resource group
        self.rg1_iam = cf.ResourceGroup("rg1_iam")

        # declare policy statements
        self.stat_parameter_store = {
            "Effect": "Allow",
            "Action": "ssm:GetParameter",
            "Resource": cf.Sub(
                string="arn:aws:ssm:${aws_region}:${aws_account_id}:parameter/${parameter_name}",
                data=dict(
                    aws_region=cf.AWS_REGION,
                    aws_account_id=cf.AWS_ACCOUNT_ID,
                    parameter_name=self.env.parameter_name,
                ),
            ),
        }

        self.stat_s3_bucket_read = {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject",
                "s3:GetObjectAttributes",
                "s3:GetObjectTagging",
            ],
            "Resource": [
                f"arn:aws:s3:::{self.env.s3dir_data.bucket}",
                f"arn:aws:s3:::{self.env.s3dir_data.bucket}/{self.env.s3dir_data.key}*",
            ],
        }

        self.stat_s3_bucket_write = {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:PutObjectTagging",
                "s3:DeleteObjectTagging",
            ],
            "Resource": [
                f"arn:aws:s3:::{self.env.s3dir_data.bucket}",
                f"arn:aws:s3:::{self.env.s3dir_data.bucket}/{self.env.s3dir_data.key}*",
            ],
        }

        self.stat_sts_get_caller_identity = {
            "Effect": "Allow",
            "Action": "sts:GetCallerIdentity",
            "Resource": "*"
        }

        self.stat_a2i_allow_list = {
            "Effect": "Allow",
            "Action": [
                "sagemaker:ListHumanLoops",
                "sagemaker:ListWorkteams",
                "sagemaker:ListWorkforces",
                "sagemaker:DescribeWorkteam",
                "sagemaker:DescribeWorkforce",
            ],
            "Resource": "*",
        }

        self.stat_a2i_allow_hil = {
            "Effect": "Allow",
            "Action": [
                "sagemaker:DescribeHumanLoop",
                "sagemaker:DeleteHumanLoop",
                "sagemaker:StartHumanLoop",
                "sagemaker:StopHumanLoop",
                "sagemaker:DescribeWorkforce",
                "sagemaker:DescribeWorkteam",
            ],
            "Resource": [
                cf.Sub(
                    string="arn:aws:sagemaker:${aws_region}:${aws_account_id}:flow-definition/${flow_name}",
                    data=dict(
                        aws_region=cf.AWS_REGION,
                        aws_account_id=cf.AWS_ACCOUNT_ID,
                        flow_name=self.env.flow_definition_name,
                    )
                ),
                cf.Sub(
                    string="arn:aws:sagemaker:${aws_region}:${aws_account_id}:human-loop/${hil_name_prefix}",
                    data=dict(
                        aws_region=cf.AWS_REGION,
                        aws_account_id=cf.AWS_ACCOUNT_ID,
                        hil_name_prefix=self.env.flow_id,
                    )
                ),
                "arn:aws:sagemaker:us-east-1:{{ cookiecutter.aws_account_id }}:workforce/*",
                "arn:aws:sagemaker:us-east-1:{{ cookiecutter.aws_account_id }}:workteam/*",
            ],
        }

        # declare Lambda IAM role
        self.iam_role_for_lambda = iam.Role(
            "IamRoleForLambda",
            rp_AssumeRolePolicyDocument=cf.helpers.iam.AssumeRolePolicyBuilder(
                cf.helpers.iam.ServicePrincipal.awslambda(),
            ).build(),
            p_RoleName=cf.Sub(
                string="${prefix}-${aws_region}-lambda",
                data=dict(
                    prefix=self.env.prefix_name_snake,
                    aws_region=cf.AWS_REGION,
                ),
            ),
            p_ManagedPolicyArns=[
                cf.helpers.iam.AwsManagedPolicy.AWSLambdaBasicExecutionRole,
            ],
        )
        self.rg1_iam.add(self.iam_role_for_lambda)

        self.output_iam_role_lambda_arn = cf.Output(
            "IamRoleLambdaArn",
            Value=self.iam_role_for_lambda.rv_Arn,
        )
        self.rg1_iam.add(self.output_iam_role_lambda_arn)

        self.iam_inline_policy_for_lambda = iam.Policy(
            "IamInlinePolicyForLambda",
            rp_PolicyName=cf.Sub(
                string="${prefix}-${aws_region}-lambda",
                data=dict(
                    prefix=self.env.prefix_name_snake,
                    aws_region=cf.AWS_REGION,
                ),
            ),
            rp_PolicyDocument=self.encode_policy_document(
                [
                    self.stat_parameter_store,
                    self.stat_s3_bucket_read,
                    self.stat_s3_bucket_write,
                    self.stat_sts_get_caller_identity,
                    self.stat_a2i_allow_list,
                    self.stat_a2i_allow_hil,
                ]
            ),
            p_Roles=[
                self.iam_role_for_lambda.ref(),
            ],
            ra_DependsOn=self.iam_role_for_lambda,
        )
        self.rg1_iam.add(self.iam_inline_policy_for_lambda)

        # declare human loop IAM role
        self.iam_role_for_human_review_workflow = iam.Role(
            "IamRoleForHumanReviewWorkflow",
            rp_AssumeRolePolicyDocument=cf.helpers.iam.AssumeRolePolicyBuilder(
                cf.helpers.iam.ServicePrincipal.sagemaker(),
            ).build(),
            p_RoleName=cf.Sub(
                string="${prefix}-${aws_region}-a2i-flow",
                data=dict(
                    prefix=self.env.prefix_name_snake,
                    aws_region=cf.AWS_REGION,
                ),
            ),
        )
        self.rg1_iam.add(self.iam_role_for_human_review_workflow)

        self.output_iam_role_for_human_review_workflow_arn = cf.Output(
            "IamRoleForHumanReviewWorkflowArn",
            Value=self.iam_role_for_human_review_workflow.rv_Arn,
        )
        self.rg1_iam.add(self.output_iam_role_for_human_review_workflow_arn)

        self.iam_inline_policy_for_human_review_workflow = iam.Policy(
            "IamInlinePolicyForHumanReviewWorkflow",
            rp_PolicyName=cf.Sub(
                string="${prefix}-${aws_region}-a2i-flow",
                data=dict(
                    prefix=self.env.prefix_name_snake,
                    aws_region=cf.AWS_REGION,
                ),
            ),
            rp_PolicyDocument=self.encode_policy_document(
                [
                    self.stat_s3_bucket_read,
                    self.stat_s3_bucket_write,
                ]
            ),
            p_Roles=[
                self.iam_role_for_human_review_workflow.ref(),
            ],
            ra_DependsOn=self.iam_role_for_human_review_workflow,
        )
        self.rg1_iam.add(self.iam_inline_policy_for_human_review_workflow)
