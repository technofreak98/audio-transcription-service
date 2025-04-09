resource "helm_release" "karpenter" {
  name       = "karpenter"
  repository = "https://charts.karpenter.sh"
  chart      = "karpenter"
  namespace  = "karpenter"
  create_namespace = true
  version    = "0.32.0"
  values = [
    file("${path.module}/karpenter-values.yaml")
  ]
}
