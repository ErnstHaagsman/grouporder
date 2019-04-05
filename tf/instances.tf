variable "key" {
  type = "string"
}

variable "aws_region" {
  type = "string"
}

provider "aws" {
  region = "${var.aws_region}"
}

data "aws_ami" "ubuntu_1604" {
  most_recent = true

  filter {
    name = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]  # Canonical's owner ID
}

resource "aws_security_group" "management_host" {
  name        = "management_host"
  description = "Allow inbound SSH traffic"
  vpc_id      = "${aws_vpc.grouporder_vpc.id}"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "web" {
  name        = "web"
  description = "Allow inbound HTTP and HTTPS traffic"
  vpc_id      = "${aws_vpc.grouporder_vpc.id}"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    security_groups = [
      "${aws_security_group.management_host.id}"
    ]
    description = "Inbound SSH traffic from management host only"
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Incoming HTTP traffic"
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "db" {
  name        = "database"
  description = "Allow internal DB and SSH traffic"
  vpc_id      = "${aws_vpc.grouporder_vpc.id}"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    security_groups = [
      "${aws_security_group.management_host.id}"
    ]
    description = "Inbound SSH traffic"
  }

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [
      "${aws_security_group.management_host.id}",
      "${aws_security_group.web.id}"
    ]
    description = "PostgreSQL"
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "management" {
  ami = "${data.aws_ami.ubuntu_1604.id}"
  instance_type = "t2.micro"

  key_name = "${var.key}"

  subnet_id = "${aws_subnet.public_subnet.id}"

  vpc_security_group_ids = [
    "${aws_security_group.management_host.id}"
  ]

  tags {
    Name = "Management Host"
  }

  depends_on = ["aws_nat_gateway.nat"]

  provisioner "file" {
    content = "${data.template_file.inventory.rendered}"
    destination = "/home/ubuntu/inventory"

    connection {
      user = "ubuntu"
      agent = true
    }
  }

  provisioner "file" {
    destination = "/home/ubuntu/.ansible.cfg"
    source = "ansible.cfg"

    connection {
      user = "ubuntu"
      agent = true
    }
  }

  provisioner "file" {
    destination = "/home/ubuntu/deploy.yml"
    source = "deploy.yml"

    connection {
      user = "ubuntu"
      agent = true
    }
  }

  provisioner "remote-exec" {
    script = "install.sh"

    connection {
      user = "ubuntu"
      agent = true
    }
  }
}

resource "aws_instance" "database" {
  ami = "${data.aws_ami.ubuntu_1604.id}"
  instance_type = "t2.micro"

  key_name = "${var.key}"

  subnet_id = "${aws_subnet.private_subnet.id}"

  vpc_security_group_ids = [
    "${aws_security_group.db.id}"
  ]

  tags {
    Name = "Grouporder Database"
  }
}

resource "aws_instance" "web" {
  ami = "${data.aws_ami.ubuntu_1604.id}"
  instance_type = "t2.micro"

  key_name = "${var.key}"

  subnet_id = "${aws_subnet.public_subnet.id}"

  vpc_security_group_ids = [
    "${aws_security_group.web.id}"
  ]

  tags {
    Name = "Grouporder Web"
  }
}

