#!/bin/sh
# Xcode Cloud runs this right after it clones the repo. The iOS project pulls
# its Capacitor plugins from node_modules and ships the built website inside
# the app, and neither is committed to git. So install Node, install the
# packages, build the site, and sync it into the iOS project before Xcode
# resolves packages and builds.
set -e

export HOMEBREW_NO_INSTALL_CLEANUP=1
export HOMEBREW_NO_AUTO_UPDATE=1
brew install node@22
export PATH="$(brew --prefix node@22)/bin:$PATH"

cd "$CI_PRIMARY_REPOSITORY_PATH"
node -v
npm ci
npm run build
npx cap sync ios
