import json

import click

import awsutil


@click.command()
@click.option('--stack-name', help='The stack name', prompt=True)
@click.option('--output-key', help='The output key', prompt=True)
def get_stack_output(stack_name, output_key):
    click.echo(awsutil.get_stack_output(stack_name, output_key))


@click.command()
@click.option('--stack-name', help='The stack name', prompt=True)
def get_stack_outputs(stack_name):
    click.echo(json.dumps(awsutil.get_stack_outputs(stack_name), indent=2))


@click.command()
@click.option('--bucket-name', help='The bucket name', prompt=True)
def empty_bucket(bucket_name):
    click.echo(awsutil.empty_bucket(bucket_name))


@click.command()
@click.option('--bucket-name', help='The bucket name', prompt=True)
def nuke_bucket(bucket_name):
    click.echo(awsutil.nuke_bucket(bucket_name))


@click.group()
def cli():
    pass


cli.add_command(get_stack_output)
cli.add_command(get_stack_outputs)
cli.add_command(empty_bucket)
cli.add_command(nuke_bucket)
