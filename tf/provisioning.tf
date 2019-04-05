data "template_file" "inventory" {
  template = "${file("inventory.tmpl")}"
  vars = {
    database_private_ip = "${aws_instance.database.private_ip}",
    web_private_ip = "${aws_instance.web.private_ip}"
  }
}

data "template_file" "ssh_config" {
  template = "${file("ssh_config.tmpl")}"
  vars = {
    database_private_ip = "${aws_instance.database.private_ip}",
    web_private_ip = "${aws_instance.web.private_ip}"
    management_public_ip = "${aws_instance.management.public_ip}"
  }
}

resource "local_file" "ssh_config" {
  content = "${data.template_file.ssh_config.rendered}"
  filename = "ssh_config.out"
}
