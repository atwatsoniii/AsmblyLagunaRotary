# Asmbly Laguna Rotary

Post processors and related files for Laguna CNC machines with B5X / Laguna IQ control, including rotary (4th axis) configurations.

## Contents

- **Laguna_IQ_Turner.cps** – Fusion / CAM post for Laguna IQ Turner (rotary along X).
- **Laguna_IQ_Shift_RevA.cps** – Fusion / CAM post for Laguna IQ Shift.
- **Autodesk_laguna_vanilla.cps** – Base Laguna post from Autodesk (Fusion / CAM).
- **B5X_Motion_Control_System.txt** – Reference for G/M codes, axis behavior, and control conventions used when editing posts.
- **Vcarve/** – VCarve Pro post and docs:
  - **Laguna_IQ_Turner_Vcarve.pp** – VCarve post for the Turner.
  - **Laguna_IQ_Turner_Vcarve_proposed.pp** – Proposed variant (rotary Y→A) for later use.

## Requirements

- Laguna CNC with B5X / Laguna IQ control.
- For Fusion posts: Autodesk Fusion (or compatible CAM) with post processor support.
- For VCarve posts: VCarve Pro (or compatible) with rotary/wrapped job setup.

## Usage

1. Copy the appropriate `.cps` (Fusion) or `.pp` (VCarve) into your CAM post folder or use the post selection in your CAM software.
2. Use **B5X_Motion_Control_System.txt** as the authority for G/M codes and axis behavior when changing or validating posts.

## License

See [LICENSE](LICENSE).
