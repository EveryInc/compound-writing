# Onboarding Flow Tests

## New User With A Specific X Task

Given a project without `voice.md` or `TASTE.md` and a user asking to write an
X post:

1. The system explains that brief setup can preserve the user's voice.
2. It asks only the cross-format voice questions needed to propose
   `voice.md`.
3. It previews the proposed `voice.md` before writing.
4. After approval, it offers `style-guides/x.md`, not all platform guides.
5. It does not create strategy files unless the user asks for platform or
   positioning work.
6. It returns to drafting the X post.

## New User Who Wants Cross-Platform Strategy

Given a user asking for a public writing strategy:

1. The system creates or confirms `voice.md` first.
2. It explains that strategy is distinct from voice.
3. It may offer `strategy/professional-positioning.md` and
   `strategy/platform-strategy.md` after preview and approval.
4. It offers destination guides only for platforms the user wants to use.

## Existing `voice.md`

Given a project already containing `voice.md`, `/scribe` should load it and
proceed. It should not rerun first-time onboarding.

## Existing Legacy Profile

Given a project with only `TASTE.md`, `/scribe` should offer legacy fallback
or reviewed migration, not create a new conflicting voice file automatically.

## Pass Criteria

- Every durable file is previewed before creation.
- A user can stop after `voice.md` and still begin writing.
- Strategy remains optional and distinct from voice.
- The original user request is resumed after setup.
