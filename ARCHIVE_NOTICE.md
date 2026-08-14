# Archive notice

This repository was superseded and archived on August 13, 2026.

## Replacements

- [awesome-nba-data](https://github.com/JovaniPink/awesome-nba-data) is the maintained public
  source and tooling catalog.
- [nba-lab](https://github.com/JovaniPink/nba-lab) is the private, two-person, fixture-backed
  product and governed data-contract repository.

NBA Lab v1 does not copy or depend on this Flask/Connexion service. It has no public HTTP API and
does not carry forward the placeholder `Person` routes, Nginx deployment shape, or legacy samples.

## Archive safety review

Reviewed August 13, 2026 before the owner archive action:

- local and GitHub code searches found no external runtime consumer; the one public profile link
  was changed to the maintained catalog;
- GitHub reported no releases, deployments, environments, or Pages site;
- the only Actions workflow is repository-local CI, not a deployment or downstream trigger;
- no published package was identified as a consumer or release boundary;
- all Git history, tests, migrations, and design evidence remain preserved.

Archiving is intentionally non-destructive: no repository deletion, history rewrite, or data copy
is part of this decision.
