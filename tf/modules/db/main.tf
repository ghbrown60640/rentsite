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
  # engine_mode        = "serverless"
  database_name   = "rentsite"
  master_username = "rentsite"
  master_password = "rentsite"
  # scaling_configuration {
  #   min_capacity = 2
  #   max_capacity = 8
  # }
  final_snapshot_identifier = "rentsite"
  db_subnet_group_name      = aws_db_subnet_group.rentsite-db-sg.name
  skip_final_snapshot       = true
  vpc_security_group_ids    = [module.network.postgres-sg.id]

}
resource "aws_rds_cluster_instance" "rentsite-db-instances" {
  count               = 2
  identifier          = "rentsite-db-${count.index}"
  cluster_identifier  = aws_rds_cluster.rentsite-db.id
  instance_class      = "db.r5.large"
  engine              = aws_rds_cluster.rentsite-db.engine
  engine_version      = aws_rds_cluster.rentsite-db.engine_version
  publicly_accessible = true
}
# resource "aws_route53_record" "rentsitedb" {
#   zone_id = module.network.route53_zone.id
#   name    = "db.rentsite.glennsbuilds.me"
#   type    = "A"
#   ttl     = 300
#   records = [aws_rds_cluster.rentsite-db.endpoint]
# }
