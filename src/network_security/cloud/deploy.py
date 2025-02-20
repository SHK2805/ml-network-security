import sys

import boto3
from botocore.exceptions import ClientError

from src.network_security.constants.cloud_pipeline import *
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger


class CloudFormationManager:
    def __init__(self, cfm_region_name=region_name,
                       cfm_stack_name=stack_name,
                       cfm_s3_bucket_name=s3_bucket_name,
                       cfm_key_pair_name=key_pair_name,
                       cfm_ecr_name=ecr_repository_name):
        """Initialize the CloudFormationManager with AWS clients."""
        self.cf_client = boto3.client('cloudformation', region_name=cfm_region_name)
        self.logs_client = boto3.client('logs', region_name=cfm_region_name)
        self.s3_client = boto3.client('s3', region_name=cfm_region_name)
        self.stack_name = cfm_stack_name
        self.bucket_name = cfm_s3_bucket_name
        self.key_pair_name = cfm_key_pair_name
        self.ecr_repository_name = cfm_ecr_name
        logger.info(f"CloudFormationManager object initialized with stack name: "
                    f"{self.stack_name} "
                    f"bucket name: {self.bucket_name} "
                    f"ECR repository name: {self.ecr_repository_name} "
                    f"region: {cfm_region_name}")

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
        """Create or update the CloudFormation stack."""
        if self.stack_exists():
            logger.info(f"Stack {self.stack_name} exists. Attempting to update.")
            try:
                response = self.cf_client.update_stack(
                    StackName=self.stack_name,
                    TemplateBody=template_body,
                    Parameters=[
                        {
                            'ParameterKey': 'BucketName',
                            'ParameterValue': self.bucket_name
                        },
                        {
                            'ParameterKey': 'ECRRepositoryName',
                            'ParameterValue': self.ecr_repository_name
                        },
                        {
                            'ParameterKey': 'KeyPairName',
                            'ParameterValue': self.key_pair_name
                        }
                    ],
                    Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM']
                )
                logger.info(f"Updating {self.stack_name} stack...")
                waiter = self.cf_client.get_waiter('stack_update_complete')
                waiter.wait(StackName=self.stack_name)
                logger.info(f"Stack {self.stack_name} updated successfully.")
            except ClientError as e:
                if 'No updates are to be performed' in str(e):
                    logger.info(f"No updates are to be performed for the stack {self.stack_name}.")
                else:
                    logger.error(f"Error updating stack {self.stack_name}: {e}")
                    raise CustomException(e, sys)
        else:
            logger.info(f"Stack {self.stack_name} does NOT exist. Starting creation.")
            try:
                response = self.cf_client.create_stack(
                    StackName=self.stack_name,
                    TemplateBody=template_body,
                    Parameters=[
                        {
                            'ParameterKey': 'BucketName',
                            'ParameterValue': self.bucket_name
                        },
                        {
                            'ParameterKey': 'ECRRepositoryName',
                            'ParameterValue': self.ecr_repository_name
                        }
                    ],
                    Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM']
                )
                logger.info(f"Creating {self.stack_name} stack...")
                waiter = self.cf_client.get_waiter('stack_create_complete')
                waiter.wait(StackName=self.stack_name)
                logger.info(f"Stack {self.stack_name} created successfully.")
                self.print_stack_outputs()
                # ecr_repository_uri = self.get_stack_output('ECRRepositoryUri')
                # logger.info(f"ECR Repository URI: {ecr_repository_uri}")
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
        """Print the stack outputs."""
        try:
            response = self.cf_client.describe_stacks(StackName=self.stack_name)
            stack = response['Stacks'][0]
            outputs = stack.get('Outputs', [])
            for output in outputs:
                logger.info(f"Stack output {output['OutputKey']}: {output['OutputValue']}")
        except ClientError as e:
            logger.error(f"Error retrieving stack outputs: {e}")
            raise CustomException(e, sys)

    def get_stack_output(self, output_key):
        """Get a specific output from the stack."""
        try:
            response = self.cf_client.describe_stacks(StackName=self.stack_name)
            stack = response['Stacks'][0]
            outputs = stack.get('Outputs', [])
            for output in outputs:
                if output['OutputKey'] == output_key:
                    logger.info(f"Stack output {output_key}: {output['OutputValue']}")
                    return output['OutputValue']

            logger.info(f"Stack output {output_key} not found.")
            return None
        except ClientError as e:
            logger.error(f"Error retrieving stack outputs: {e}")
            raise CustomException(e, sys)

# Main function
def main():
    if not cf_template_file_name:
        logger.info(f"CloudFormation template file not found: {cf_template_file_name}")
        return
    with open(cf_template_file_name, 'r') as template_file:
        template_body = template_file.read()

    cf_manager = CloudFormationManager()
    cf_manager.create_stack(template_body)
    logger.info(f"CloudFormation stack creation completed with "
                f"region: {region_name}, stack name: {stack_name}"
                f"bucket name: {s3_bucket_name}"
                f"ecr repo name {ecr_repository_name}.")
    # print the stack outputs
    cf_manager.print_stack_outputs()
    # Uncomment the line below to delete the stack
    # cf_manager.delete_stack()

if __name__ == "__main__":
    main()
