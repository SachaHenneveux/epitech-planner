"""CLI entry point for Credit Strategy tool."""

import argparse
import sys
from pathlib import Path

import requests

from . import __version__
from .api import EpitechAPI
from .excel import generate_excel


def main():
    parser = argparse.ArgumentParser(
        description="Generate Excel timeline of Epitech projects for credit planning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m credit_strategy --cookie "gdpr=1; euconsent-v2=...; user=..."
    python -m credit_strategy --cookie "..." --semester 3

To get your cookie:
    1. Log in to https://intra.epitech.eu
    2. Open DevTools (F12 or Cmd+Option+I)
    3. Go to Network tab, filter by "filter" or "format=json"
    4. Click on a request to intra.epitech.eu
    5. In Headers > Request Headers, copy the full "Cookie" value
        """
    )
    parser.add_argument(
        "--cookie", "-c",
        required=True,
        help="Full cookie string from request headers"
    )
    parser.add_argument(
        "--semester", "-s",
        type=int,
        default=None,
        help="Semester number (default: latest available)"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output Excel file path (default: output/credit_strategy_S{semester}.xlsx)"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Credit Strategy Tool - Epitech Timeline Generator")
    print("=" * 60)

    # Initialize API
    api = EpitechAPI(args.cookie)

    # Test connection and get modules list
    print("\nConnecting to intranet...")
    try:
        raw_modules = api.get_modules_list()
        print(f"  Connection OK - {len(raw_modules)} modules found")
    except requests.exceptions.HTTPError as e:
        print(f"  HTTP ERROR {e.response.status_code}: {e.response.reason}")
        if e.response.status_code == 403:
            print("  -> Invalid or expired cookie")
            print("  -> Please get a new cookie from the intranet")
        elif e.response.status_code == 503:
            print("  -> Epitech server temporarily unavailable")
            print("  -> Try again in a few minutes")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"  Connection ERROR: {e}")
        sys.exit(1)

    # Fetch user info
    print("\nFetching user info...")
    try:
        user_info = api.get_user_info()
        year_credits = user_info.credits % 60  # Credits for current year
        print(f"  {user_info.name} - Year {user_info.student_year} (Promo {user_info.promo})")
        print(f"  Total credits: {user_info.credits} | This year: {year_credits}/60 | GPA: {user_info.gpa}")
    except Exception as e:
        print(f"  Warning: Could not fetch user info: {e}")
        user_info = None

    # Auto-detect latest semester if not specified
    if args.semester is None:
        semesters = {m.get("semester") for m in raw_modules if m.get("semester")}
        args.semester = max(semesters) if semesters else 1
        print(f"  Auto-detected latest semester: {args.semester}")

    # Calculate year semesters (Year 1 = S1-S2, Year 2 = S3-S4, etc.)
    # First semester of year: (year - 1) * 2 + 1
    # Second semester of year: (year - 1) * 2 + 2
    year_credits_data = {}
    if user_info:
        first_sem = (user_info.student_year - 1) * 2 + 1
        second_sem = first_sem + 1

        print(f"\nFetching year {user_info.student_year} credits (S{first_sem}-S{second_sem})...")

        # Always fetch first semester of the year
        print(f"  Scanning S{first_sem}...", end=" ", flush=True)
        s1_data = api.fetch_semester_credits(first_sem)
        year_credits_data[first_sem] = s1_data
        print(f"validated={s1_data['validated']}, pending={s1_data['pending']}")

        # Fetch second semester only if we're in it (current semester >= second_sem)
        if args.semester >= second_sem:
            print(f"  Scanning S{second_sem}...", end=" ", flush=True)
            s2_data = api.fetch_semester_credits(second_sem)
            year_credits_data[second_sem] = s2_data
            print(f"validated={s2_data['validated']}, pending={s2_data['pending']}")

    # Set output path now that we know the semester
    if args.output is None:
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        args.output = str(output_dir / f"credit_strategy_S{args.semester}.xlsx")

    # Fetch modules for timeline
    modules = api.fetch_all_modules(args.semester)

    if not modules:
        print(f"\nNo modules found for semester {args.semester}")
        sys.exit(0)

    # Generate Excel
    generate_excel(modules, args.output, args.semester, user_info, year_credits_data)

    print("\n" + "=" * 60)
    print("Done!")
    print(f"  - {len(modules)} modules exported")
    print(f"  - File: {args.output}")
    print("=" * 60)


if __name__ == "__main__":
    main()
