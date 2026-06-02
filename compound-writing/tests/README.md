# Verification Plan

These are product-promise tests rather than implementation unit tests. They
describe what a writer should be able to trust before the public core ships.

| Promise to the user | Contract to verify |
| --- | --- |
| "I can start without building a whole brand system." | [`onboarding-flow.md`](onboarding-flow.md): setup creates only approved, immediately useful files. |
| "The plugin reads only what applies to this assignment." | [`workspace-loading.md`](workspace-loading.md): style and strategy context loads selectively. |
| "My existing workspace will not be silently rearranged." | [`migration-contract.md`](migration-contract.md): legacy migration is previewed and reversible in practice. |
| "The system cannot decide permanent preferences for me." | [`improvement-loop.md`](improvement-loop.md): durable learning always needs approval. |
| "The shipped defaults do not contain someone else's personal context." | [`public-boundary.md`](public-boundary.md): templates are portable and examples are synthetic or cleared. |

Release testing should exercise these promises with a fresh user project, a
legacy project, and an attempted unapproved update.
