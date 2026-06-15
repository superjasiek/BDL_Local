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

## API Limits

The script is designed to respect the GUS BDL API rate limits for anonymous users (5 requests/second). If you have an API key, you can modify the script to include it in the headers for higher limits.
