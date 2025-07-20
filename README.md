Place a file called `.env` in this directory and add your Google Generative-AI key:

```
GOOGLE_API_KEY=YOUR_ACTUAL_KEY_HERE
```

Then, with [uv](https://docs.astral.sh/uv/) installed, start the project:

```bash
uv sync         # installs everything listed in uv.lock & pyproject.toml
uv run python main.py
```

That’s it—`uv.lock` and `pyproject.toml` are already present; no manual `pip install` needed.
