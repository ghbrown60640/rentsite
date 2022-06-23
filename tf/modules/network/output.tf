output "public_subnets" {
  value = aws_subnet.rentsite-public-subnet.*.id
}
output "route53_zone" {
  value = aws_route53_zone.rentsite
}
output "postgres-sg" {
  value = aws_security_group.postgres-sg
}
