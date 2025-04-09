resource "aws_sqs_queue" "processing" {
  name                      = "audio-processing-queue"
  visibility_timeout_seconds = 300
  message_retention_seconds = 86400
}

resource "aws_sqs_queue" "dlq" {
  name = "audio-dlq"
}

resource "aws_sqs_queue_policy" "policy" {
  queue_url = aws_sqs_queue.processing.id
  policy    = data.aws_iam_policy_document.sqs_policy.json
}

data "aws_iam_policy_document" "sqs_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com", "transcribe.amazonaws.com"]
    }
    actions = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.processing.arn]
  }
}
