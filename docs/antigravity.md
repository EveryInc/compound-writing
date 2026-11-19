# Compound Writing in Google Antigravity

Antigravity loads Compound Writing as a native plugin from `.antigravity-plugin/plugin.json`. The complete repository is the plugin: `skills/` supplies the writing workflows, `references/` supplies the shared context contract, and `defaults/` supplies generic writing-home templates. Install the whole directory so those relative paths remain intact.

## Install

Use a current Antigravity version with native plugin support. The packaging checks were verified with Antigravity CLI 1.5.11. Install Python 3 if you want Scribe to create a writing home.

Clone the public repository into a new directory, then install that checkout:

```bash
git clone https://github.com/EveryInc/compound-writing.git
agy plugin validate ./compound-writing
agy plugin install ./compound-writing
agy plugin list --json
```

The CLI installs plugins under `~/.gemini/config/plugins/`, shared by the Antigravity App, CLI, and IDE. In the App, inspect **Customizations > Installed**; in the IDE, use **Customizations** in the agent side panel. Verify that `compound-writing` is enabled and its skills include `cw-scribe`.

Start a new conversation in your writing workspace and select `cw-scribe` from the slash picker, or ask to use `cw-scribe`. Plugin skills may appear with a namespace, such as `compound-writing:cw-scribe`; use the entry shown by your host. Specialist skills such as `cw-draft` and `cw-voice-check` are also available. In the interactive CLI, `/skills` shows loaded skills and their source paths; `/skills reload` refreshes discovery.

The `commands/` directory contains Claude-only compatibility commands. Antigravity's validator warns that it ignores this directory; that warning is expected. Use `/cw-scribe` to begin, or ask it to explain the toolbox, instead of relying on `/cw-help` or `/cw-commands`. Antigravity also leaves the nested Claude subagent adapters unloaded; panels and debates use the matching reviewer skills or available isolated workers.

### Workspace-only installation

For a plugin available only in one project, clone the whole repository inside that project's `.agents/plugins/` directory instead of using the global installer:

```bash
mkdir -p /path/to/writing-workspace/.agents/plugins
git clone https://github.com/EveryInc/compound-writing.git \
  /path/to/writing-workspace/.agents/plugins/compound-writing
```

Open that workspace in Antigravity and start a new conversation. Choose either workspace or global installation to avoid duplicate skill discovery. Do not copy only `skills/` into `.agents/skills/`: shared references and templates live outside individual skill directories.

## Context and writing files

Keep `VOICE.md`, `STYLE.md`, optional `AUDIENCE.md`, examples, and drafts in your writing workspace. The plugin contains generic templates only. Scribe reads the active workspace's instructions and applicable host rules before choosing a workflow. `GEMINI.md` can name existing shared guides, just as `AGENTS.md` can; no extra rule file is required for installation.

Writing-home setup resolves the bundled script relative to its `SKILL.md` and writes to a separately resolved destination. It refuses a non-empty destination unless adding missing files was requested, and preserves existing files. Learning belongs in maintained writing context, never in the installed plugin.

## Update or remove

For a local-checkout installation, update the source checkout with `git pull --ff-only`, validate it again, then rerun `agy plugin install /path/to/compound-writing` and follow any replacement prompt. Check `agy plugin list --json` and start a new conversation. For a workspace clone, update that clone and reload the workspace's skills.

To remove a CLI-installed copy, run `agy plugin uninstall compound-writing`. For a workspace installation, remove only the `.agents/plugins/compound-writing` checkout after preserving any local changes. Your writing home remains separate from either installation.

## Verify a change

From the repository root, using Python 3.9 or later for the tests:

```bash
python3 -m unittest discover -s tests -v
agy plugin validate . --json
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

The Antigravity packaging tests check metadata agreement across hosts, shared skill/resource paths, relocated writing-home setup, and loader discovery when `agy` is installed. They accept only the known `commands/` warning. `agy plugin validate --strict .` fails on that warning by design; ordinary validation must have no errors or other warnings. Validation reads the package without installing it or running a model.

After installing, manually verify:

1. `cw-scribe` appears in the host's skills list with the expected plugin path, and slash invocation loads it.
2. Scribe can read a disposable workspace's `VOICE.md` and `STYLE.md` through the context contract.
3. Requested setup creates a separate disposable writing home; optional audience setup preserves an existing guide.
4. A reviewer skill loads; panel/debate execution uses the workers available in that host and reports any missing reviewer output.

## Host conventions

This adapter uses native skills and the multi-provider plugin manifest described in Google's [plugin authoring guide](https://antigravity.google/docs/build-plugins). Installation locations and commands follow the [plugin guide](https://antigravity.google/docs/plugins); invocation and discovery follow the [skills guide](https://antigravity.google/docs/skills) and [customization discovery guide](https://antigravity.google/docs/customization-discovery). These conventions were checked on 2026-11-19. Antigravity's [workflow migration guide](https://antigravity.google/docs/migration/workflows-to-skills) recommends skills for new integrations, so this package does not generate duplicate workflow files.
