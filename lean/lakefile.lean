import Lake
open Lake DSL

package «mathtools» where
  version := "0.1.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_library «MathTools» where
  roots := #[`MathTools]
