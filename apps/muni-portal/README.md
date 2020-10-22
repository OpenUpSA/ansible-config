## Production example

Modify User ARN and bucket name for other environments.

```json
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "PublicReadForGetBucketObjects-original_images",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::muni-portal-backend/original_images/*"
    },
    {
      "Sid": "PublicReadForGetBucketObjects-images",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::muni-portal-backend/images/*"
    },
    {
      "Sid": "PublicReadForGetBucketObjects-documents",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::muni-portal-backend/documents/*"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::567304594100:user/cape-agulhas-app"
      },
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::muni-portal-backend",
        "arn:aws:s3:::muni-portal-backend/*"
      ]
    }
  ]
}
```