---
name: Focused Minimalist
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#393939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#c7c4d7'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#908fa0'
  outline-variant: '#464554'
  surface-tint: '#c0c1ff'
  primary: '#c0c1ff'
  on-primary: '#1000a9'
  primary-container: '#8083ff'
  on-primary-container: '#0d0096'
  inverse-primary: '#494bd6'
  secondary: '#b9c8de'
  on-secondary: '#233143'
  secondary-container: '#39485a'
  on-secondary-container: '#a7b6cc'
  tertiary: '#ffb783'
  on-tertiary: '#4f2500'
  tertiary-container: '#d97721'
  on-tertiary-container: '#452000'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#d4e4fa'
  secondary-fixed-dim: '#b9c8de'
  on-secondary-fixed: '#0d1c2d'
  on-secondary-fixed-variant: '#39485a'
  tertiary-fixed: '#ffdcc5'
  tertiary-fixed-dim: '#ffb783'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#703700'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  h1:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  h2:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.75'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.01em
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1.4'
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  container-max: 1120px
  content-width: 720px
  gutter: 24px
  margin-mobile: 16px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
  stack-xl: 80px
---

## Brand & Style
This design system centers on intellectual focus and digital quietude. It is designed for a target audience of long-form readers and writers who value clarity over decoration. The emotional response should be one of calm, professional authority and modern sophistication.

The design style is a blend of **Minimalism** and **Modern Corporate** aesthetics. It utilizes heavy whitespace—or "darkspace"—to separate ideas, ensuring that the content remains the absolute protagonist. The interface recedes into the background, employing subtle depth cues to guide the user without distracting from the reading experience.

## Colors
The palette is built on a foundation of deep charcoal and slate to reduce eye strain during extended reading sessions. 

- **Backgrounds**: Use `#121212` for the primary canvas and `#181818` for elevated surfaces like cards or navigation bars.
- **Accents**: A muted violet (`#6366F1`) serves as the primary action color, providing a sophisticated point of interest that contrasts against the dark base without appearing garish.
- **Typography**: Primary text uses an off-white (`#F8FAFC`) to maintain high contrast while avoiding the harshness of pure white. Secondary information utilizes slate (`#94A3B8`) to establish a clear visual hierarchy.

## Typography
This design system uses **Inter** exclusively to maintain a utilitarian, systematic feel. The focus is on the "Body-LG" style, which features a generous 1.75 line-height to maximize readability for long-form articles. 

Headlines use tighter line-heights and slight negative letter-spacing to appear cohesive and "locked-in" at larger scales. Use the "Label" styles for metadata such as read times, categories, and dates, ensuring they are distinct from the narrative flow of the body text.

## Layout & Spacing
The layout follows a **Fixed Grid** philosophy for content reading, centering the text within a 720px "sweet spot" to prevent long line lengths that fatigue the eye. The overall container max-width is 1120px for gallery or dashboard views.

A vertical rhythm based on an 8px/4px scale ensures consistency. Use `stack-xl` for section breaks and `stack-md` for internal component spacing. On mobile, margins shrink to 16px, and the layout collapses into a single-column stack, maintaining the same generous vertical breathing room between elements.

## Elevation & Depth
Depth is conveyed through **Tonal Layers** and **Low-Contrast Outlines**. Instead of heavy shadows, surfaces are differentiated by their background color (shifting from `#121212` to `#181818`).

- **Borders**: Elements like cards and inputs use a subtle 1px border (`#262626`) to define their boundaries against the dark background.
- **Shadows**: When necessary for floating elements like dropdowns, use a large-radius, low-opacity shadow (e.g., `blur: 40px, opacity: 0.4, color: #000000`).
- **Interactive Depth**: Buttons may use a very soft glow effect using the primary accent color when hovered, creating a sense of "light" rather than "physical weight."

## Shapes
The shape language is **Soft**. A base radius of 4px (`0.25rem`) is applied to most UI components, including buttons and input fields. Larger elements like cards or featured images use a `rounded-lg` (8px) radius. This subtle rounding prevents the interface from feeling too aggressive while maintaining the disciplined, structured look of a professional publication.

## Components
- **Buttons**: Primary buttons are filled with the accent violet, using white text for maximum legibility. Secondary buttons use a slate outline and no fill.
- **Cards**: Use the `#181818` surface color with a 1px `#262626` border. Padding should be generous (min 24px) to keep content centered and clear.
- **Input Fields**: Ghost-style inputs with a bottom border or a subtle full-border in slate. Focus states should transition the border color to the primary accent violet.
- **Chips/Tags**: Small, low-contrast pills using a slate background at 10% opacity with slate text. These should be unobtrusive.
- **Article Lists**: Clean rows with a thin divider or subtle vertical spacing. Use high-contrast headers and muted metadata labels.
- **Progress Bar**: A slim 2px accent-colored line at the top of the viewport to indicate reading progress without obstructing the header.