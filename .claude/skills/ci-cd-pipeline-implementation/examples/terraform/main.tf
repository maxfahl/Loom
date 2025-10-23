resource "aws_s3_bucket" "example" {
  bucket = "my-unique-example-bucket-12345"
  acl    = "private"

  tags = {
    Environment = "Development"
    Project     = "CI-CD-Demo"
  }
}

resource "aws_s3_bucket_object" "index_html" {
  bucket = aws_s3_bucket.example.id
  key    = "index.html"
  source = "./static/index.html"
  content_type = "text/html"
}

output "bucket_name" {
  value = aws_s3_bucket.example.bucket
}