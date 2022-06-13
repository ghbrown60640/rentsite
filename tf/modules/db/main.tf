module "network" {
  source = "../network"
}
resource "aws_db_subnet_group" "rentsite-db-sg" {
  name       = "rentsite-db-sg"
  subnet_ids = module.network.public_subnets

  tags = {
    Name = "rentsite-db-sg"
  }
}
resource "aws_rds_cluster" "rentsite-db" {
  cluster_identifier = "rentsite-db"
  engine             = "aurora-postgresql"
  engine_mode        = "serverless"
  database_name      = "rentsite"
  master_username    = "rentsite"
  master_password    = "rentsite"
  scaling_configuration {
    min_capacity = 2
    max_capacity = 8
  }
  final_snapshot_identifier = "rentsite"
  db_subnet_group_name      = aws_db_subnet_group.rentsite-db-sg.name
  skip_final_snapshot       = false
  # backup_retention_period = 5
  # preferred_backup_window = "07:00-09:00"
}
# resource "aws_rds_cluster_instance" "rentsite-cluster-instances" {
#   count              = 2
#   identifier         = "aurora-cluster-demo-${count.index}"
#   cluster_identifier = aws_rds_cluster.rentsite-db.id
#   instance_class     = "db.m6i.large"
#   engine             = aws_rds_cluster.rentsite-db.engine
#   engine_version     = aws_rds_cluster.rentsite-db.engine_version
# }
