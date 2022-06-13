module "west" {
  source = "./modules/us-west-2"
}
module "east" {
  source = "./modules/us-east-2"
}
# resource "aws_db_subnet_group" "default" {
#   name       = "main"
#   subnet_ids = [aws_subnet.public_subnet.*.id]
#
#   tags = {
#     Name = "My DB subnet group"
#   }
# }
