import boto3


def restore_deleted_files(bucket_name: str, prefix: str) -> None:
    s3_client = boto3.client('s3')

    paginator = s3_client.get_paginator('list_object_versions')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in page_iterator:
        if 'DeleteMarkers' in page:
            for delete_marker in page['DeleteMarkers']:
                if delete_marker['IsLatest']:
                    key = delete_marker['Key']
                    version_id = delete_marker['VersionId']

                    print(f'Restoring {key} (version: {version_id})')
                    # Remove the delete marker to restore the object
                    s3_client.delete_object(
                        Bucket=bucket_name,
                        Key=key,
                        VersionId=version_id
                    )


if __name__ == "__main__":
    bucket = "my-bucket"
    folder_prefix = "deleted_folder/"
    restore_deleted_files(bucket, folder_prefix)
