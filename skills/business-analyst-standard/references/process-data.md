# Process And Data

Use this reference for workflows, states, data fields, permissions, and integrations.

## Process Flow

For workflows, capture:

- Trigger.
- Actor.
- Main path.
- Alternate paths.
- Error/recovery paths.
- End state.

Simple format:

```text
1. Admin opens Package screen.
2. Admin selects published locations and audios.
3. System validates required language coverage.
4. System generates package.
5. Package status becomes Ready for publish.
```

## States And Transitions

When a feature has statuses, define allowed transitions and who can perform them.

```text
Draft -> Published: Admin only, requires required fields.
Published -> Archived: Admin only, hides from mobile sync.
Archived -> Published: Admin only, requires validation again.
```

## Data Requirements

For each important entity/field, capture:

- Name and meaning.
- Required/optional.
- Type/format/limits.
- Default value.
- Validation.
- Source of truth.
- Visibility by role/channel.
- Migration/backfill needs.

## Permissions

Define permissions as business rules, not only UI behavior.

```text
Editors can create and update draft content.
Only admins can publish, archive, or delete content.
Mobile users can read only published content included in the latest package.
```

## Integrations

For integrations, capture source, destination, trigger, payload, frequency, failure handling, retries, and audit/logging expectations.
