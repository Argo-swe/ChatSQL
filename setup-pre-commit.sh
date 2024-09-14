#!/bin/bash

# Assicurati che pre-commit sia installato
if ! command -v pre-commit &> /dev/null
then
    echo "pre-commit non trovato, installazione in corso..."
    pip install pre-commit
fi

# Installa gli hook definiti in .pre-commit-config.yaml
#pre-commit install
