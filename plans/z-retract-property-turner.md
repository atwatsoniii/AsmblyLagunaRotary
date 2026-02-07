# Add Properties for Z Retract (Turner)

## Goal

Add two user-facing properties in [Fusion/Laguna_IQ_Turner.cps](Fusion/Laguna_IQ_Turner.cps):

1. **When** to retract Z before a work plane (rotary) change: always, skip for pattern operations only, or never.
2. **Retract Z value**: the Z position (in WCS, job units) to retract to, so users can retract to a high safe height instead of fixed Z0.

## Current behavior

- In **setWorkPlane()** (lines 512–517): the post retracts Z (to WCS Z0) before changing work plane **unless** the current section is a pattern operation. So pattern ops never trigger a Z retract; all other work plane changes do.
- In **writeRetract()** (lines 1265–1268): Z retract always outputs D0 then G0 Z0 (hardcoded 0).

## Proposed properties

### 1. When to retract before work plane change

**Name:** `retractZBeforeWorkPlane`

**Type:** enum

**Options:**

| Value ID          | Title                       | Behavior                                                                                  |
| ----------------- | --------------------------- | ----------------------------------------------------------------------------------------- |
| `always`          | Always retract              | Retract Z before every work plane change when not already retracted (safest, most moves). |
| `skipForPatterns` | Skip for pattern operations | Current behavior: retract unless the section is a pattern operation.                      |
| `never`           | Never retract               | Do not retract Z before work plane change (fewest moves; user must ensure clearance).     |

**Default:** `skipForPatterns` (preserves current behavior).

**Description:** "When to retract Z to safe height before rotating the table. 'Always' retracts every time; 'Skip for pattern operations' avoids retract between pattern instances; 'Never' disables retract before rotation."

### 2. Retract Z value (safe height)

**Name:** `retractZHeight`

**Type:** number (real)

**Default:** 0 (current behavior: retract to WCS Z0).

**Units:** Same as the job (mm or inch). Use the post's `unit` variable; no conversion needed if the value is entered in job units.

**Description:** "Z position (in work coordinates) to retract to. 0 = Z0 in the work coordinate system (WCS); set a positive value (e.g. 10 mm or 0.5 in) to retract to a safe height above the part. Applies to all Z retracts (before work plane change, tool change, end of program)."

This value is used in **writeRetract()** whenever Z is retracted: output G0 Z&lt;retractZHeight&gt; instead of G0 Z0. So "always retract" can retract to a high Z if the user sets e.g. 10 mm or 0.5 in.

## Implementation steps

1. **Add both properties and definitions** in [Laguna_IQ_Turner.cps](Fusion/Laguna_IQ_Turner.cps):
   - In **properties** (lines 36–44): add `retractZBeforeWorkPlane: "skipForPatterns"` and `retractZHeight: 0`.
   - In **propertyDefinitions** (lines 47–54): add the enum entry for `retractZBeforeWorkPlane` (title, description, group, type "enum", values) and the number entry for `retractZHeight` (title, description, group, type "number" or "double", default 0). Use the same group (e.g. "retract" or group 1) for both so they appear together.
2. **Use retractZBeforeWorkPlane in setWorkPlane()** (lines 512–517):
   - Keep the existing `isPatternOperation` computation.
   - Replace the condition `if (!retracted && !isPatternOperation)` with logic that:
     - If property is **always**: retract when `!retracted`.
     - If **skipForPatterns**: retract when `!retracted && !isPatternOperation` (current behavior).
     - If **never**: do not call `writeRetract(Z)` in this block.
   - Read via `properties.retractZBeforeWorkPlane`.
3. **Use retractZHeight in writeRetract()** (lines 1265–1268):
   - Replace the hardcoded `zOutput.format(0)` with `zOutput.format(properties.retractZHeight)` (or a local variable set from the property). If the property is undefined, fall back to 0 so existing behavior is preserved.
4. **Optional:** Short comments above the condition in setWorkPlane() and in writeRetract() explaining that behavior is driven by these properties.

## Files to change

- [Fusion/Laguna_IQ_Turner.cps](Fusion/Laguna_IQ_Turner.cps) only: property block, `setWorkPlane()`, and `writeRetract()`.

## Testing

- **retractZBeforeWorkPlane:** Set to Skip for pattern operations / Always / Never and verify Z retract (or no retract) before work plane change as described. With Always and a pattern, every rotation should have a retract.
- **retractZHeight:** Set to 0: output should be G0 Z0 as today. Set to e.g. 10 (mm) or 0.5 (in): all Z retracts (before rotation, tool change, end) should output G0 Z10 or G0 Z0.5 respectively.
