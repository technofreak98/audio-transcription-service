resource "aws_s3_bucket" "audio_bucket" {
  bucket = "mental-audio-bucket"
  force_destroy = true
}
