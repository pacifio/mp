#!/bin/bash

function_code='
function mp() {
  if [ -z "$1" ]; then
    echo "Usage: mp -i <file.md>"
    return 1
  fi
  python3 '"$(pwd)"'/mp.py "$@"
}
'

if [ -f "$HOME/.zshrc" ]; then
  profile_file="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
  profile_file="$HOME/.bashrc"
else
  echo "No suitable profile file found."
  exit 1
fi

if grep -q "function mp() {" "$profile_file"; then
  echo "Function 'mp' is already present in $profile_file"
else
  # Insert the function into the profile file
  echo "$function_code" >> "$profile_file"
  echo "Function 'mp' has been added to $profile_file"
fi

if [ "$profile_file" = "$HOME/.bashrc" ]; then
  source "$HOME/.bashrc"
elif [ "$profile_file" = "$HOME/.zshrc" ]; then
  source "$HOME/.zshrc"
fi
