#!/bin/bash
# Script to safe push changes to GitHub

# Add backend/myenv to .gitignore if not present (handled by agent, but good for safety)
if ! grep -q "backend/myenv/" .gitignore; then
    echo "backend/myenv/" >> .gitignore
fi

# Add all changes
git add .

# Commit changes
echo "Committing changes..."
git commit -m "Update upload behavior, fix server offline error, and add deployment config"

# Pull remote changes with rebase to handle divergence
echo "Pulling remote changes..."
git pull --rebase origin master

# Push to remote
echo "Pushing to GitHub..."
git push origin master

echo "Done!"
