resource "aws_vpc" "grouporder_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
}

resource "aws_internet_gateway" "main" {
  vpc_id = "${aws_vpc.grouporder_vpc.id}"
}

resource "aws_egress_only_internet_gateway" "main" {
  vpc_id = "${aws_vpc.grouporder_vpc.id}"
}

resource "aws_subnet" "public_subnet" {
  vpc_id = "${aws_vpc.grouporder_vpc.id}",
  cidr_block = "10.0.0.0/24"
  map_public_ip_on_launch = true
}

resource "aws_route_table" "public_table" {
  vpc_id = "${aws_vpc.grouporder_vpc.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.main.id}"
  }

  route {
    ipv6_cidr_block = "::/0"
    egress_only_gateway_id = "${aws_egress_only_internet_gateway.main.id}"
  }
}

resource "aws_route_table_association" "public_table_association" {
  subnet_id = "${aws_subnet.public_subnet.id}"
  route_table_id = "${aws_route_table.public_table.id}"
}

resource "aws_eip" "nat" {
  vpc = true
  depends_on = ["aws_internet_gateway.main"]
}

resource "aws_nat_gateway" "nat" {
  subnet_id = "${aws_subnet.public_subnet.id}"
  allocation_id = "${aws_eip.nat.id}"

  depends_on = ["aws_internet_gateway.main"]
}

resource "aws_subnet" "private_subnet" {
  vpc_id = "${aws_vpc.grouporder_vpc.id}",
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = false
}


resource "aws_route_table" "private_table" {
  vpc_id = "${aws_vpc.grouporder_vpc.id}"

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = "${aws_nat_gateway.nat.id}"
  }

  route {
    ipv6_cidr_block = "::/0"
    egress_only_gateway_id = "${aws_egress_only_internet_gateway.main.id}"
  }
}

resource "aws_route_table_association" "private_table_association" {
  subnet_id = "${aws_subnet.private_subnet.id}"
  route_table_id = "${aws_route_table.private_table.id}"
}
