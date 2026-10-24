# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Run all tests: `python3 -m unittest discover -s tests -v`
- Run single test file: `python3 -m unittest tests.test_risk -v`
- Load module from folder: `PYTHONPATH=trader-india python3 -c 'import india; ...'`
- Config check: `python3 -c 'import json; c=json.load(open("trader-india/config.india.json")); ...'`

## Architecture

11 skill folders (trader-scanner, trader-news, trader-entry, trader-exit, trader-timemachine, trader-risk, trader-budget, trader-broker, trader-alerts, trader-analyst, trader-pelosi) + tests/. Each skill is self-contained Python with standard library only. Order flow: scanner -> entry -> exit -> budget -> risk -> broker. New India module: trader-india/ with india.py, __init__.py, config.india.json.

## Key notes

- Paper trading default (`paper: true` in config). No live orders without explicit user yes + risk PASS.
- Tests use fixtures (tests/fixtures/) and mock broker responses. No real orders or live credentials in tests.
- India module uses regex-based contract validation; contracts must match format (e.g., NIFTY22050CE). Config has duplicate `broker` key (string and object) that needs merge.
