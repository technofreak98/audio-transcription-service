provider "aws" {
  region = var.aws_region
}

module "network" {
  source = "./network"
}

module "eks" {
  source      = "./eks"
  vpc_id      = module.network.vpc_id
  subnet_ids  = module.network.subnet_ids
  cluster_name = var.cluster_name
}

module "services" {
  source = "./services"
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}
