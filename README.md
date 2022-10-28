# deploy-bot
This action manages deployments by creating deployment PRs between a designated source and target branch.

The action first creates a deployment branch, from the source branch, named `deployment/%m-%d-%Y`. Then, a PR is created, targeting the target branch from the source branch. All contributors to the PR are added as reviewers.

## Example Workflow
An example workflow is shown below. This workflow runs the `deploy-bot` every weekday at 9AM ET.

```yaml
name: deploy-bot

on:
  schedule:
    - cron: 0 13 * * 1-5

jobs:
    deploy:
        steps:
            - uses: ryansingman/deploy-bot@1.0.0
              with:
                source: staging
                target: main
                pr_body: "Daily deplyoment PR :robot:"
```
