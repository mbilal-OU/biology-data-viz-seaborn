# Environment Setup

## macOS and Linux

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m pip install -e .
```

If local PowerShell policy blocks activation, call the environment interpreter
directly without changing machine policy:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m jupyter lab
```

## Verify

```bash
pytest -q
python scripts/build_advanced_gallery.py
```
