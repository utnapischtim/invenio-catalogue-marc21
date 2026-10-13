#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

# Usage:
#  ./run-tests.sh

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

python -m pytest
