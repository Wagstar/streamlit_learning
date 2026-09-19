#!/usr/bin/env bash
# This script is used to start the application.

set -e

cd "$(dirname "${BASH_SOURCE[0]}")"
source ./.venv/bin/activate
streamlit run main.py --server.port 8503
