import sys

import boto3
import botocore
from botocore.exceptions import ClientError

from src.network_security.constants.cloud_pipeline import s3_region, s3_stack_name, s3_bucket_name, s3_cf_template
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger


class CloudFormationManager:
    def __init__(self, region_name, stack_name, bucket_name):
        """Initialize the CloudFormationManager with AWS clients."""
        self.cf_client = boto3.client('cloudformation', region_name=region_name)
        self.logs_client = boto3.client('logs', region_name=region_name)
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.stack_name = stack_name
        self.bucket_name = bucket_name
        logger.info(f"CloudFormationManager initialized with stack name: {stack_name} and bucket name: {bucket_name}")

    def stack_exists(self):
        """Check if the stack exists."""
        stacks = self.cf_client.list_stacks(
            StackStatusFilter=[
                'CREATE_IN_PROGRESS', 'CREATE_FAILED', 'CREATE_COMPLETE',
                'ROLLBACK_IN_PROGRESS', 'ROLLBACK_FAILED', 'ROLLBACK_COMPLETE',
                'DELETE_FAILED', 'UPDATE_IN_PROGRESS', 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
                'UPDATE_COMPLETE', 'UPDATE_FAILED', 'UPDATE_ROLLBACK_IN_PROGRESS',
                'UPDATE_ROLLBACK_FAILED', 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS',
                'UPDATE_ROLLBACK_COMPLETE', 'REVIEW_IN_PROGRESS', 'IMPORT_IN_PROGRESS',
                'IMPORT_COMPLETE', 'IMPORT_ROLLBACK_IN_PROGRESS', 'IMPORT_ROLLBACK_FAILED',
                'IMPORT_ROLLBACK_COMPLETE'
            ]
        )
        for stack in stacks['StackSummaries']:
            if stack['StackName'] == self.stack_name:
                logger.info(f"Stack {self.stack_name} exists.")
                return True
        logger.info(f"Stack {self.stack_name} does NOT exist.")
        return False

    def create_stack(self, template_body):
        """Create the CloudFormation stack."""
        if self.stack_exists():
            logger.info(f"Stack {self.stack_name} already exists. Skipping creation.")
            return

        logger.info(f"Stack {self.stack_name} does NOT exist. Starting creation.")
        try:
            response = self.cf_client.create_stack(
                StackName=self.stack_name,
                TemplateBody=template_body,
                Parameters=[
                    {
                        'ParameterKey': 'BucketName',
                        'ParameterValue': self.bucket_name
                    }
                ],
                Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM']
            )
            logger.info(f"Creating {self.stack_name} stack...")
            waiter = self.cf_client.get_waiter('stack_create_complete')
            waiter.wait(StackName=self.stack_name)
            logger.info(f"Stack {self.stack_name} created successfully.")
            self.print_stack_outputs()
        except ClientError as e:
            logger.error(f"Error creating stack {self.stack_name}: {e}")
            raise CustomException(e, sys)

    def delete_stack(self):
        """Delete the CloudFormation stack."""
        try:
            response = self.cf_client.delete_stack(StackName=self.stack_name)
            logger.info(f"Deleting {self.stack_name} stack...")
            waiter = self.cf_client.get_waiter('stack_delete_complete')
            waiter.wait(StackName=self.stack_name)
            logger.info(f"Stack {self.stack_name} deleted successfully.")
            self.delete_log_groups()
        except ClientError as e:
            logger.error(f"Error deleting stack: {e}")
            raise CustomException(e, sys)

    def delete_log_groups(self):
        """Delete associated log groups."""
        try:
            log_groups = self.logs_client.describe_log_groups(
                logGroupNamePrefix=self.stack_name
            )
            for log_group in log_groups['logGroups']:
                log_group_name = log_group['logGroupName']
                self.logs_client.delete_log_group(logGroupName=log_group_name)
                logger.info(f"Deleted log group: {log_group_name}")
        except ClientError as e:
            logger.error(f"Error deleting log groups: {e}")
            raise CustomException(e, sys)

    def print_stack_outputs(self):
        """Print the outputs of the stack."""
        try:
            response = self.cf_client.describe_stacks(StackName=self.stack_name)
            stack = response['Stacks'][0]
            outputs = stack.get('Outputs', [])
            for output in outputs:
                logger.info(f"{output['OutputKey']}: {output['OutputValue']}")
        except ClientError as e:
            logger.error(f"Error retrieving stack outputs: {e}")
            raise CustomException(e, sys)

# Main function
def main():
    if not s3_cf_template:
        logger.info(f"CloudFormation template file not found: {s3_cf_template}")
        return
    with open(s3_cf_template, 'r') as template_file:
        template_body = template_file.read()

    cf_manager = CloudFormationManager(s3_region, s3_stack_name, s3_bucket_name)
    cf_manager.create_stack(template_body)
    logger.info(f"CloudFormation stack creation completed with "
                f"region: {s3_region}, stack name: {s3_stack_name}, bucket name: {s3_bucket_name}.")
    # Uncomment the line below to delete the stack
    # cf_manager.delete_stack()

if __name__ == "__main__":
    main()
