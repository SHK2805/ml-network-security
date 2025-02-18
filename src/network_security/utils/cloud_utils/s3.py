import os

class S3Sync:
    def __init__(self, local_dir: str, aws_bucket_url: str):
        self.class_name = self.__class__.__name__
        self.local_dir = local_dir
        self.bucket_name = aws_bucket_url.split("/")[2]
        self.s3_dir = "/".join(aws_bucket_url.split("/")[3:])
        self.aws_bucket_url = aws_bucket_url

    def sync_to_s3(self):
        os.system(f"aws s3 sync {self.local_dir} {self.aws_bucket_url}")

    def sync_from_s3(self):
        os.system(f"aws s3 sync {self.aws_bucket_url} {self.local_dir}")