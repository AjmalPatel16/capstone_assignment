provider "aws" {
  region = "ap-south-1"   # Mumbai region 
}

# Security group to allow SSH and HTTP
resource "aws_security_group" "allow_http_ssh" {
  name        = "allow_http_ssh"
  description = "Allow HTTP (8000) and SSH (22)"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "FastAPI"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance
resource "aws_instance" "app" {
  ami           = "ami-0dee22c13ea7a9a67" # Ubuntu 22.04 LTS (Mumbai). Change for your region if needed.
  instance_type = "t2.micro"
  key_name      = "my-key" # This must match the key pair you created in AWS

  vpc_security_group_ids = [aws_security_group.allow_http_ssh.id]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y docker.io
              systemctl start docker
              systemctl enable docker
              docker run -d -p 8000:8000 ajmalpatel/housing-fastapi:latest
              EOF

  tags = {
    Name = "mlops-capstone-app"
  }
}
