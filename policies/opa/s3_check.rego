package main

import rego.v1

# Rule: Deny S3 buckets with public read access
deny if {
    input.resource_type == "aws_s3_bucket"
    input.properties.acl == "public-read"
}

# Rule: Deny S3 buckets missing server-side encryption
deny if {
    input.resource_type == "aws_s3_bucket"
    not input.properties.server_side_encryption_configuration
}