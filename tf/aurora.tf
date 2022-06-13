# resource "aws_db_subnet_group" "default" {
#   name       = "main"
#   subnet_ids = [aws_subnet.public_subnet.*.id]
#   depends_on = [aws_subnet.public_subnet]
#
#   tags = {
#     Name = "My DB subnet group"
#   }
# }
# resource "aws_rds_cluster" "rentsite_db" {
#   cluster_identifier      = "rentsite-db"
#   engine                  = "aurora-postgresql"
#   availability_zones      = ["us-west-2a", "us-west-2b", "us-west-2c"]
#   database_name           = "rentsite"
#   master_username         = "rentsite"
#   master_password         = "rentsite"
#   backup_retention_period = 5
#   preferred_backup_window = "07:00-09:00"
# }
