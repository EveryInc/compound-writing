# Workspace Loading Tests

## Longform

Given a project with `voice.md`, `style-guides/longform.md`, and strategy
files, a request to line-edit an essay should load voice and longform style.
It should not require social strategy unless positioning is part of the ask.

## X

Given an X adaptation request, the system should load `voice.md`,
`style-guides/x.md`, source material, and optional platform strategy. It
should not impose longform structure.

## LinkedIn

Given a LinkedIn draft request concerning professional positioning, the system
should load `voice.md`, `style-guides/linkedin.md`, and the relevant strategy
file.

## Pass Criteria

- The assistant identifies the intended destination.
- Only relevant layered files are used.
- Missing optional files cause an offer to create or proceed without them,
  rather than invented guidance.

