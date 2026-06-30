---
name: Mathematical Logic System
colors:
  surface: '#f8f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f8f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#454652'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#767683'
  outline-variant: '#c6c5d4'
  surface-tint: '#4c56af'
  primary: '#000666'
  on-primary: '#ffffff'
  primary-container: '#1a237e'
  on-primary-container: '#8690ee'
  inverse-primary: '#bdc2ff'
  secondary: '#48626e'
  on-secondary: '#ffffff'
  secondary-container: '#cbe7f5'
  on-secondary-container: '#4e6874'
  tertiary: '#380b00'
  on-tertiary: '#ffffff'
  tertiary-container: '#5c1800'
  on-tertiary-container: '#e17c5a'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e0e0ff'
  primary-fixed-dim: '#bdc2ff'
  on-primary-fixed: '#000767'
  on-primary-fixed-variant: '#343d96'
  secondary-fixed: '#cbe7f5'
  secondary-fixed-dim: '#afcbd8'
  on-secondary-fixed: '#021f29'
  on-secondary-fixed-variant: '#304a55'
  tertiary-fixed: '#ffdbd0'
  tertiary-fixed-dim: '#ffb59d'
  on-tertiary-fixed: '#390c00'
  on-tertiary-fixed-variant: '#7b2e12'
  background: '#f8f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  math-display:
    fontFamily: Source Serif 4
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  sidebar-width: 280px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  unit: 8px
---

## Brand & Style
The design system is engineered for rigor, precision, and sustained intellectual focus. It serves an academic and technical audience that requires high information density without cognitive fatigue. 

The visual style is **Modern Minimalism** with a **Corporate/Institutional** lean. It prioritizes content clarity above all else, utilizing generous whitespace to separate logic blocks and a strict adherence to a systematic grid. The aesthetic is "quiet" to allow the complexity of the mathematics to be the focal point, evoking the feeling of a clean, digital chalkboard or a well-set academic journal.

## Colors
This design system utilizes a palette rooted in "Oxford Blue" (Primary) to establish authority and depth. 

- **Primary (#1A237E):** Used for navigation headers, primary actions, and branding elements.
- **Secondary (#546E7A):** A muted Slate used for secondary text, icons, and non-critical UI borders to maintain a calm environment.
- **Accent (#00B8D4):** A high-visibility Cyan reserved strictly for active states, focus indicators, and highlighting specific steps in a resolution.
- **Backgrounds:** The primary surface is pure white (#FFFFFF), with background offsets in very light grays (#F5F7F9) to distinguish toolbars and sidebars from the main workspace.

## Typography
The system employs a dual-font strategy: **Inter** handles the functional UI layer for maximum legibility at small sizes, while **Source Serif 4** provides a "Computer Modern" aesthetic for mathematical expressions, ensuring they feel distinct from the application interface.

- **UI Elements:** Use Inter for all buttons, labels, and navigation. 
- **Mathematical Expressions:** Use Source Serif 4 for rendered equations and symbolic logic. It provides the necessary contrast and academic weight.
- **Symbolic Input/Code:** Use JetBrains Mono for raw input strings and logical proofs to ensure character alignment and distinction between similar glyphs (e.g., 0 and O).

## Layout & Spacing
The layout follows a **Fixed-Fluid hybrid** model. A fixed-width left sidebar (280px) houses the primary tool navigation, while the main workspace expands to a maximum of 1280px to maintain readable line lengths for proofs.

- **Grid:** A 12-column grid is used within the workspace.
- **Rhythm:** An 8px linear scale governs all padding and margins (8, 16, 24, 32, 48, 64).
- **Mobile:** On mobile devices, the sidebar collapses into a bottom sheet or a full-screen drawer. The workspace margins reduce to 16px.

## Elevation & Depth
To maintain an academic, "flat" aesthetic, this design system avoids heavy shadows. Depth is communicated via **Tonal Layers** and **Low-Contrast Outlines**.

- **Level 0 (Base):** Light gray background (#F5F7F9) for the application shell.
- **Level 1 (Workspace):** White (#FFFFFF) surfaces with 1px solid borders (#E0E4E8).
- **Level 2 (Popovers/Modals):** Pure white with a very soft, subtle 8px blur shadow (5% opacity, Primary color tint) to distinguish from the workspace.
- **Focus:** Use the Accent Cyan color for 2px solid outlines on active input fields.

## Shapes
The shape language is **Soft**. A 0.25rem (4px) base radius is applied to buttons and inputs, providing a modern feel without appearing too "playful" or consumer-oriented. This subtle rounding maintains the precision of a grid-based academic layout while softening the overall user experience. Large containers like cards or proof blocks use `rounded-lg` (8px).

## Components
- **Sidebar:** The primary navigation hub. Use a dark theme (Primary color background) for the sidebar even in light mode to clearly separate "Tools" from "Work."
- **Buttons:**
  - *Primary:* Solid Oxford Blue with white text. No gradients.
  - *Secondary:* Ghost style with Primary color border and text.
  - *Action:* Small, icon-heavy buttons for mathematical symbols.
- **Expression Blocks:** Rendered math should be centered in cards with a subtle gray background (#F9FAFB) and a left-accent border using the Secondary color.
- **Offline Indicator:** A persistent, small pill in the status bar. Use a soft Sage Green dot for "Online/Synced" and a simple neutral gray for "Offline Mode" to avoid unnecessary visual alarm.
- **Inputs:** Use monospaced fonts for logical input fields to ensure clarity of brackets and variables. Labels should use `label-caps` for a professional, organized look.
- **Status Indicators:** Use the Primary color for "Processing" and the Accent Cyan for "Solved/Active."