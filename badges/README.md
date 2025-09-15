# 🛠️ Compiler/OS Dashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/<your-org>/<your-repo>/ci.yml?branch=master)](https://github.com/<your-org>/<your-repo>/actions)

This repository contains an automated dashboard showing build/test status across multiple **compilers** and **Linux distributions**.  
The table is generated dynamically from JSON job results (`badge-status/*.json`) by the Python script `generate_dashboard.py`.

##  Dashboard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/vargaconsulting/github-runner-test/gh-pages/badges/dashboard-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/vargaconsulting/github-runner-test/gh-pages/badges/dashboard-light.svg">
  <img alt="Compiler/OS Matrix" src="https://raw.githubusercontent.com/vargaconsulting/github-runner-test/gh-pages/badges/dashboard-light.svg">
</picture>

## 🚀 Usage

### Generate the dashboards

```bash
# Collect JSON results from CI and generate SVG dashboards
./generate_dashboard.py
