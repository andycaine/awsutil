import json

import click

from awsutil import cf
from awsutil import s3


@click.command()
@click.option('--stack-name', help='The stack name', prompt=True)
@click.option('--output-key', help='The output key', prompt=True)
@click.option('--region', help='The region', prompt=False, default=None)
def get_stack_output(stack_name, output_key, region):
    click.echo(cf.get_stack_output(stack_name, output_key, region))


@click.command()
@click.option('--stack-name', help='The stack name', prompt=True)
@click.option('--region', help='The region', prompt=False, default=None)
def get_stack_outputs(stack_name, region):
    click.echo(json.dumps(cf.get_stack_outputs(stack_name, region),
                          indent=2))


@click.command()
@click.option('--bucket-name', help='The bucket name', prompt=True)
def empty_bucket(bucket_name):
    click.echo(s3.empty_bucket(bucket_name))


@click.command()
@click.option('--bucket-name', help='The bucket name', prompt=True)
def nuke_bucket(bucket_name):
    click.echo(s3.nuke_bucket(bucket_name))


@click.command()
@click.option('--template',
              help='The template - can be local file or https URL',
              prompt=True)
@click.option('--stack-name', help='The stack name', prompt=True)
@click.option('--cfn-exec-role', help='The role to execute CloudFormation',
              prompt=False, default=None)
@click.option('--deploy-role', help='The role assumed by CloudFormation for '
              'deployment operations', prompt=False, default=None)
@click.option('--region', help='The region', prompt=False, default=None)
@click.option('--iam', help='Whether to add the IAM capability', prompt=False,
              default=False, is_flag=True)
@click.option('--auto-expand',
              help='Whether to add the AUTO_EXPAND capability', prompt=False,
              default=False, is_flag=True)
@click.option('--param', help='The parameters to pass to CloudFormation',
              prompt=False, default=None, type=(str, str), multiple=True)
def cfn_deploy(template, stack_name, cfn_exec_role, deploy_role,
               region, param, iam, auto_expand):
    capabilities = []
    if iam:
        capabilities.append('CAPABILITY_IAM')
    if auto_expand:
        capabilities.append('CAPABILITY_AUTO_EXPAND')

    params = []
    for k, v in param:
        params.append(dict(
            ParameterKey=k,
            ParameterValue=v
        ))

    cf.deploy(
        template=template,
        stack_name=stack_name,
        cfn_exec_role=cfn_exec_role,
        deploy_role=deploy_role,
        region=region,
        params=params,
        capabilities=capabilities
    )


@click.group()
def cli():
    pass


cli.add_command(get_stack_output)
cli.add_command(get_stack_outputs)
cli.add_command(empty_bucket)
cli.add_command(nuke_bucket)
cli.add_command(cfn_deploy)
