import boto3


def _cfn_client(region=None, role=None):
    kwargs = region and {'region_name': region} or {}

    if role:
        sts = boto3.client('sts')
        session_name = f'awsutil-{role}'
        credentials = sts.assume_role(
            RoleArn=role,
            RoleSessionName=session_name
        )['Credentials']

        kwargs.update({
            'aws_access_key_id': credentials['AccessKeyId'],
            'aws_secret_access_key': credentials['SecretAccessKey'],
            'aws_session_token': credentials['SessionToken']
        })

    return boto3.client('cloudformation', **kwargs)


def get_stack_output(stack_name, output_key, region=None):
    cfn = _cfn_client(region)
    response = cfn.describe_stacks(StackName=stack_name)
    stack = response['Stacks'][0]
    outputs = stack['Outputs']
    for output in outputs:
        if output['OutputKey'] == output_key:
            return output['OutputValue']
    return None


def get_stack_outputs(stack_name, region=None):
    cfn = _cfn_client(region)
    response = cfn.describe_stacks(StackName=stack_name)
    stack = response['Stacks'][0]
    outputs = stack['Outputs']
    return outputs


def deploy(stack_name, template, cfn_exec_role=None, deploy_role=None,
           region=None, params={}, capabilities=[]):
    cfn = _cfn_client(region=region, role=cfn_exec_role)

    deploy_args = dict(
        StackName=stack_name,
        Parameters=params,
        Capabilities=capabilities
    )
    if deploy_role:
        deploy_args['RoleARN'] = deploy_role

    if template.startswith('https'):
        deploy_args['TemplateURL'] = template
    else:
        with open(template, 'r') as file:
            template_body = file.read()
            deploy_args['TemplateBody'] = template_body

    if _stack_exists(cfn, stack_name):
        waiter = _update_stack(cfn, deploy_args)
    else:
        waiter = _create_stack(cfn, deploy_args)

    if waiter:
        waiter.wait(StackName=stack_name)


def _stack_exists(cfn, stack_name):
    stacks = cfn.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackName'] == stack_name:
            return True
    return False


def _create_stack(cfn, deploy_args):
    cfn.create_stack(**deploy_args)
    return cfn.get_waiter('stack_update_complete')


def _update_stack(cfn, deploy_args):
    try:
        cfn.update_stack(**deploy_args)
        return cfn.get_waiter('stack_create_complete')
    except cfn.exceptions.ClientError as e:
        if 'No updates are to be performed' in str(e):
            return None
