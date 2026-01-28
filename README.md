# kube_homelab

A Kubernetes homelab infrastructure repository for managing local K3s cluster deployments using Helm and ArgoCD with automated configuration management.

## Overview

This repository contains the configuration and infrastructure-as-code for a personal Kubernetes homelab environment. It uses Helmfile for Helm chart management and templating, with support for multiple environments and components.

## Project Structure

```
kube_homelab/
├── README.md                              # Project documentation
├── kubeconfig.yaml                        # Kubernetes cluster configuration
├── .envrc                                 # Environment variables for direnv
├── .github/                               # GitHub workflows and agents
│   └── agents/
│       └── homelab.agent.md               # Agent configuration
├── _components/                           # Helm component templates
│   ├── argocd.gotmpl                      # ArgoCD deployment configuration
│   ├── external_secrets.yaml              # External Secrets Operator setup
│   ├── monitoring.gotmpl                  # Monitoring stack configuration
│   ├── nginx_ingress_controller.gotmpl    # NGINX Ingress Controller
│   ├── setup_helmfile.gotmpl              # Helmfile setup configuration
│   └── vault.gotmpl                       # HashiCorp Vault configuration
├── _scripts/                              # Utility scripts
│   └── generate_kubeconfig.sh             # Script to generate/update kubeconfig
└── config/                                # Configuration files
    ├── environments.yaml                  # Environment definitions
    ├── env_vars/
    │   └── all.yaml.gotmpl                # Global template variables
    └── helmfile.d/
        └── 01_init.yaml                   # Initial Helmfile configuration
```

## Key Components

### Helm Components (`_components/`)

- **argocd.gotmpl**: GitOps continuous deployment using ArgoCD
- **vault.gotmpl**: Secrets management with HashiCorp Vault
- **external_secrets.yaml**: Integration for syncing secrets from Vault
- **monitoring.gotmpl**: Monitoring and observability stack
- **nginx_ingress_controller.gotmpl**: Ingress controller for routing
- **setup_helmfile.gotmpl**: Helmfile initialization and setup

### Configuration (`config/`)

- **environments.yaml**: Defines available environments and their configurations
- **env_vars/all.yaml.gotmpl**: Global template variables used across all components
- **helmfile.d/01_init.yaml**: Main Helmfile with initial chart deployments

### Scripts (`_scripts/`)

- **generate_kubeconfig.sh**: Generates and updates kubeconfig from local K3s installation

## Prerequisites

- [Kubernetes](https://kubernetes.io/) cluster (K3s recommended)
- [Helm](https://helm.sh/) 3.x+
- [Helmfile](https://github.com/roboll/helmfile)
- [direnv](https://direnv.net/) (optional, for environment management)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/paretl/kube_homelab.git
cd kube_homelab
```

### 2. Setup Environment

```bash
# If using direnv
direnv allow

# Or manually source environment variables
source .envrc
```

### 3. Generate Kubeconfig

```bash
./_scripts/generate_kubeconfig.sh
```

### 4. Deploy Components

```bash
# Sync all Helm charts defined in helmfile
helmfile sync

# Or apply a specific component
helmfile -f config/helmfile.d/01_init.yaml sync
```

## Configuration

### Environment Variables

Edit `.envrc` to configure your environment variables. The `config/env_vars/all.yaml.gotmpl` template file uses these variables.

### Adding New Components

1. Create a new template file in `_components/` (e.g., `newcomponent.gotmpl`)
2. Reference it in `config/helmfile.d/01_init.yaml`
3. Define required values in `config/env_vars/all.yaml.gotmpl`

## Deployment

### Using Helmfile

```bash
# Preview changes (dry-run)
helmfile diff

# Apply all charts
helmfile sync

# Apply specific component
helmfile -f config/helmfile.d/01_init.yaml sync
```

### Using ArgoCD

Once ArgoCD is deployed, it will continuously sync your cluster state with this repository.

## Management

### Update Kubeconfig

```bash
./_scripts/generate_kubeconfig.sh
```

### Accessing the Cluster

```bash
kubectl --kubeconfig=./kubeconfig.yaml get nodes
```

## Secrets Management

This repository uses:
- **HashiCorp Vault** for secret storage (`vault.gotmpl`)
- **External Secrets Operator** for secret synchronization (`external_secrets.yaml`)

Ensure Vault is properly configured before deploying other components.

## Automatic README Updates

This repository uses **GitHub Actions with Claude API** to automatically update the README on each push.

### How It Works

When you push changes to `master` that affect the repository structure:

1. GitHub Actions workflow triggers automatically
2. Claude Sonnet analyzes the current directory structure
3. The "Project Structure" section in README is intelligently updated
4. Changes are automatically committed back to the repository

### Setup

To enable this feature:

1. Get your API key from [Anthropic Console](https://console.anthropic.com)
2. Add `CLAUDE_API_KEY` to your GitHub repository secrets
3. That's it! The workflow is ready to go

For detailed setup instructions, see [GITHUB_ACTIONS_SETUP.md](./GITHUB_ACTIONS_SETUP.md).

### Local Testing

You can also test locally:

```bash
export CLAUDE_API_KEY="your-key-here"
pip install anthropic
./_scripts/generate_tree.sh > /tmp/tree.txt
python ./_scripts/update_readme_with_llm.py
```

## Monitoring and Observability

The `monitoring.gotmpl` component sets up observability tools. Configure monitoring targets in `config/env_vars/all.yaml.gotmpl`.

## Troubleshooting

### Common Issues

- **Helmfile sync fails**: Ensure all Helm repositories are updated with `helm repo update`
- **Kubeconfig errors**: Run `generate_kubeconfig.sh` to regenerate
- **Template errors**: Check `config/env_vars/all.yaml.gotmpl` for missing variables

### Debugging

Enable verbose logging:

```bash
helmfile --debug sync
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Commit (pre-commit hooks will validate)
4. Push and open a pull request

## License

This project is part of a personal homelab setup. Modify as needed for your environment.

## References

- [Helmfile Documentation](https://github.com/roboll/helmfile)
- [ArgoCD Documentation](https://argoproj.github.io/argo-cd/)
- [HashiCorp Vault](https://www.vaultproject.io/)
- [K3s Documentation](https://k3s.io/)

