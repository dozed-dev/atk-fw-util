# Alienek firmware utilities

## Overview

This a collection of utilities for Alientek T80 firmware. This may work on other Alientek products, however I tested it only on T80.

It includes a reverse-engineered decryption implementation for their .atk firmware, a flashing tool, and a tool to pack raw binary to .atk (for flashing via Alientek's bootloader).

This allows you to freely flash your own code via factory bootloader, and to decrypt factory firmware for analysis and reverse-engineering.

## Getting started

```bash
python -m .venv
source .venv/bin/activate # on linux/macos
.venv/bin/Activate.ps1 # on windows
pip install poetry
poetry install
```

Now you can run `atk-fw-util`
