#!/usr/bin/env bash
git config --system --add safe.directory '*'
pre-commit run --all-files
