# Credit Strategy

Generate an Excel Gantt timeline of Epitech projects to plan your credit strategy.

## Installation

```bash
git clone https://github.com/yourusername/credit-strategy.git
cd credit-strategy
pip install -e .
```

Or without installation:

```bash
pip install requests openpyxl
```

## Usage

### Get your authentication cookie

1. Log in to https://intra.epitech.eu
2. Open DevTools (`F12` or `Cmd+Option+I`)
3. Go to the **Network** tab
4. Refresh the page or navigate to any module page
5. Look for a request containing `format=json` (e.g., `filter?format=json`)
6. Click on it, then in **Headers** > **Request Headers**
7. Find the `Cookie` line and copy the **entire value**

The cookie looks like this (very long string):
```
gdpr=1; euconsent-v2=CP...; user=eyJ0eXAi...; ...
```

### Generate timeline

```bash
# If installed
credit-strategy --cookie "gdpr=1; euconsent-v2=...; user=..."

# Without installation
python -m credit_strategy --cookie "gdpr=1; euconsent-v2=...; user=..."
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-c`, `--cookie` | Full cookie string (required) | - |
| `-s`, `--semester` | Semester number | Latest available |
| `-o`, `--output` | Output file path | `output/credit_strategy_S{semester}.xlsx` |

### Examples

```bash
# Latest semester (auto-detected)
credit-strategy -c "gdpr=1; ..."

# Specific semester
credit-strategy -c "gdpr=1; ..." -s 3

# Custom output
credit-strategy -c "gdpr=1; ..." -o ~/Desktop/timeline.xlsx
```

## Output

The Excel file contains:

- **Module column**: Project names grouped by category
- **Timeline**: Weeks with colored bars showing project periods
- **Credits**: Credit value for each module
- **Reg.**: Checkmark if you're registered

### Sections

- **Regular modules**: Grouped by category (AI, Security, DevOps, etc.)
- **Innovation**: Bonus credits (separate section at bottom)

### Totals

- **TOTAL AVAILABLE**: Sum of all module credits
- **TOTAL REGISTERED**: Sum of credits for modules you're registered in
- **TOTAL BONUS**: Innovation credits (if validated)

## Project Structure

```
credit-strategy/
├── credit_strategy/
│   ├── __init__.py     # Package exports
│   ├── __main__.py     # CLI entry point
│   ├── api.py          # Epitech API client
│   ├── config.py       # Constants and colors
│   ├── excel.py        # Excel generation
│   └── models.py       # Data models
├── output/             # Generated files (gitignored)
├── pyproject.toml
├── requirements.txt
└── README.md
```

## License

MIT
