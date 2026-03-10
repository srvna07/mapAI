# mapAI — Test Automation

Playwright + pytest, Page Object Model.

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
```

## Running

```bash
python runtests_ui.py         # UI tests
python runtests_api.py        # API tests

pytest tests/ui/test_smoke.py # smoke only
pytest -m critical            # by marker
ENV=prod python runtests_ui.py
```

## Structure

```
├── configs/            dev + prod environment config
├── pages/              page objects
├── testdata/           test input data
├── tests/
│   ├── ui/             browser tests + conftest
│   └── api/            api tests + conftest
├── utils/              shared helpers
├── conftest.py         shared fixtures
├── runtests_ui.py
└── runtests_api.py
```

## Markers

`smoke` `critical` `high` `medium` `low`
