#!/usr/bin/env bash
# install-chemacs.sh: Bootstrap CheMacs2 for Emacs profiles
set -euo pipefail

# Where to install CheMacs
CHEMACS_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/chemacs"
CHEMACS_REPO="https://github.com/plexus/chemacs.git"

if [ -d "$CHEMACS_DIR" ]; then
  echo "✅ CheMacs already installed at $CHEMACS_DIR"
  exit 0
fi

echo "🚀 Installing CheMacs2 into $CHEMACS_DIR"
git clone --depth=1 "$CHEMACS_REPO" "$CHEMACS_DIR"

echo
echo "🎉 CheMacs2 installed! Now add this to your init.el (or init.org) to bootstrap it:"
cat <<'EOF'

;; === CheMacs2 bootstrap ===
;; adjust the path if you cloned somewhere else
(let ((chemacs-init (expand-file-name "init.el" (concat
                   (or (getenv "XDG_CONFIG_HOME") "~/.config")
                   "/chemacs/"))))
  (when (file-exists-p chemacs-init)
    (load-file chemacs-init)))

;; Then: use `M-x chemacs-select-profile` to pick your profile.
;; =========================
EOF

echo
echo "Next step: run ‘chmod +x install-chemacs.sh’ and ‘./install-chemacs.sh’—let’s get those profiles loading fast!" 
