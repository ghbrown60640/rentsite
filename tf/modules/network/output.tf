output "public_subnets" {
  value = aws_subnet.rentsite-public-subnet.*.id
}
