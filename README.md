# BDL_Local

Local mirror for GUS BDL (Bank Danych Lokalnych) data.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

To initialize the database and fetch all units (territorial structure):
```bash
python3 bdl_mirror.py --units-only
```

To fetch data for a specific category (e.g., "Struktura demograficzna"):
```bash
python3 bdl_mirror.py --category "Struktura demograficzna"
```

To fetch data for a specific year range:
```bash
python3 bdl_mirror.py --category "Struktura demograficzna" --year-from 2022 --year-to 2022
```

Available categories are defined in `bdl_mirror.py` in the `VARIABLES_MAP` dictionary.

## Monthly Updates

To keep the database updated once a month, you can set up a cron job. For example, to update the population data on the 1st of every month at 3:00 AM:

```bash
0 3 1 * * /usr/bin/python3 /path/to/bdl_mirror.py --category "Struktura demograficzna" --year-from $(date +\%Y) --year-to $(date +\%Y)
```

## API Limits & Multi-Key Support

The script is designed to respect the GUS BDL API rate limits.
- Anonymous: 5 requests/second
- Registered: 10 requests/second

You can provide up to 3 API keys using the `--api-keys` argument. The script will automatically switch to the next key if a rate limit (HTTP 429) is encountered.

Example with API keys:
```bash
python3 bdl_mirror.py --category "Struktura demograficzna" --api-keys KEY1 KEY2 KEY3
```
