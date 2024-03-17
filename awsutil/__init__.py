import boto3


def _cfn_client(region=None):
    kwargs = region and {'region_name': region} or {}
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


def empty_bucket(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.objects.all().delete()
    return 'Bucket {} is now empty'.format(bucket_name)


def nuke_bucket(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()
    return 'Bucket {} is now deleted'.format(bucket_name)
