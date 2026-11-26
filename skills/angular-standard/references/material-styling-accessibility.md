# Material, Styling, And Accessibility

Use this reference for Angular Material, CDK, component styles, Tailwind, accessibility, ARIA, dialogs, tables, and animations.

## Angular Material

When editing a standalone component using Material, import every Material module used in the template.

Common mappings:

- `<mat-card>`: `MatCardModule`
- `<mat-spinner>`: `MatProgressSpinnerModule`
- `<mat-form-field>`: `MatFormFieldModule`
- `<input matInput>`: `MatInputModule`
- `<mat-select>`: `MatSelectModule`
- `<button mat-button>` / `mat-raised-button` / `mat-icon-button`: `MatButtonModule`
- `<mat-icon>`: `MatIconModule`
- `<mat-table>`: `MatTableModule`
- `<mat-paginator>`: `MatPaginatorModule`
- `<mat-sort-header>`: `MatSortModule`
- `<mat-dialog-content>` and dialogs: `MatDialogModule`
- `<mat-menu>`: `MatMenuModule`
- `<mat-tabs>`: `MatTabsModule`
- `<mat-toolbar>`: `MatToolbarModule`
- `matTooltip`: `MatTooltipModule`

If icons render as text, check whether Material Icons font or an icon registry is configured in global styles/bootstrap.

## Dialogs

Dialog components in standalone apps must import their own template dependencies just like page components.

Use typed dialog data and results where practical:

```typescript
const dialogRef = this.dialog.open(LocationDialogComponent, {
  data: { location },
});

dialogRef.afterClosed().subscribe((result: LocationFormValue | undefined) => {
  if (!result) return;
  this.save(result);
});
```

Ensure focus management, close/cancel behavior, and error handling are present for forms in dialogs.

## Tables And Lists

For operational admin screens, optimize for scanning and repeated use:

- Provide clear empty, loading, and error states.
- Use pagination or virtual scrolling for large lists.
- Keep actions predictable and aligned.
- Confirm destructive actions.
- Do not rely on color alone for status.

## Component Styling

Prefer component styles for component-specific layout and global styles for theme tokens, resets, and shared utility classes.

Avoid disabling encapsulation unless integrating with a library that requires it.

Keep fixed-format controls stable with explicit dimensions or layout constraints so dynamic labels and loading states do not shift the UI.

## Tailwind

If Tailwind is already configured, use it consistently. If adding it to an Angular project, prefer:

```bash
ng add tailwindcss
```

Do not introduce Tailwind into an established Material/CSS codebase without user intent or a clear local precedent.

## Accessibility

Use semantic HTML first. Add ARIA only when native semantics cannot express the control.

Checklist:

- Labels are associated with form controls.
- Buttons have accessible names, especially icon buttons.
- Dialogs trap focus and restore focus on close.
- Menus, tabs, accordions, comboboxes, and listboxes follow expected keyboard behavior.
- Error text is tied to controls and announced when needed.
- Color contrast is sufficient and status is not color-only.

For custom complex widgets, prefer Angular CDK or Material primitives before hand-rolling ARIA interactions.

## Animations

Prefer CSS transitions/animations for simple UI motion. Use Angular animation APIs or route transition APIs only when the project already uses them or when state-driven animation coordination is required.

Respect reduced motion preferences for non-essential animations.
