#!/bin/bash

## Update and upgrade the system
echo "Updating and upgrading the system"
sudo apt update
sudo apt ugprade -y

## Upgrade pip and install virtualenv
echo "Upgrading pip and installing virtualenv"
pip install --upgrade pip
pip install virtualenv

## Create a virtual environment
echo "Creating a virtual environment"
virtualenv .venv
