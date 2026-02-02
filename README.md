# Asmbly Laguna Rotary

Post processors and related files for Laguna CNC machines with B5X / Laguna IQ control, including rotary (4th axis) configurations.

## Contents

- **Laguna_IQ_Turner.cps** – Modified Laguna Post for Asmbly 4 axis use
- **Laguna_IQ_Shift_RevA.cps** – Normal fusion post for 3 axis use
- **Autodesk_laguna_vanilla.cps** – For reference, a post for Laguna CNCs from Autodesk
- **B5X_Motion_Control_System.txt** – Reference for G/M codes, axis behavior, and control conventions used when editing posts.
- **Vcarve/** – VCarve Pro post and docs:
  - **Laguna_IQ_Turner_Vcarve.pp** – VCarve post for 4 axis use
  - **Laguna_IQ_Turner_Vcarve_proposed.pp** – Proposed variant (rotary Y→A)
  - **Vcarve_Post_Processor_info.mhtml** - Reference information for Vcarve post processors

## Requirements

- Laguna CNC with B5X / Laguna IQ control.
- For Fusion posts: Autodesk Fusion (or compatible CAM) with post processor support.
- For VCarve posts: VCarve Pro (or compatible) with rotary/wrapped job setup.

## Setup

- In Fusion CAM, WCS origin must be along the rotary axis

## License

See [LICENSE](LICENSE).
