# coco-de-guide

The team's dbt standards, packaged as one plugin.

- **Skill:** `new-dbt-model` builds new models the team's way
- **Subagent:** `dbt-review` checks every model against the conventions and reports PASS/FAIL (read-only)
- **Hook:** blocks any `dbt ... --target prod` command (production goes through CI/CD)
