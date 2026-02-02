"""Epitech Intranet API client."""

import time
from datetime import datetime

import requests

from .config import BASE_URL, MODULES_ENDPOINT, REQUEST_HEADERS
from .models import Activity, Module, UserInfo


def parse_date(date_str: str | None) -> datetime | None:
    """Parse a date string from the API.

    Args:
        date_str: Date string in format "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"

    Returns:
        Parsed datetime object or None if invalid
    """
    if not date_str:
        return None

    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


class EpitechAPI:
    """Client for the Epitech Intranet API."""

    def __init__(self, cookie: str, max_retries: int = 3, retry_delay: int = 2):
        """Initialize the API client.

        Args:
            cookie: Authentication cookie (full cookie string or just the user token)
            max_retries: Number of retry attempts on failure
            retry_delay: Base delay between retries in seconds
        """
        self.session = requests.Session()
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Handle both full cookie string and token-only input
        if "user=" in cookie:
            self.session.headers.update({"Cookie": cookie})
        else:
            self.session.headers.update({"Cookie": f"user={cookie}; gdpr=1"})

        self.session.headers.update(REQUEST_HEADERS)

    def _request(self, url: str) -> requests.Response:
        """Make an HTTP request with automatic retries."""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=30)

                if response.status_code == 503:
                    if attempt < self.max_retries - 1:
                        print(f"\n  Server unavailable, retry {attempt + 2}/{self.max_retries}...", end="", flush=True)
                        time.sleep(self.retry_delay * (attempt + 1))
                        continue

                response.raise_for_status()
                return response

            except requests.exceptions.RequestException:
                if attempt < self.max_retries - 1:
                    print(f"\n  Network error, retry {attempt + 2}/{self.max_retries}...", end="", flush=True)
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    raise

        return response

    def get_modules_list(self, semester: int | None = None) -> list[dict]:
        """Fetch the list of available modules.

        Args:
            semester: Filter by semester number (optional)

        Returns:
            List of raw module dictionaries from the API
        """
        url = f"{BASE_URL}{MODULES_ENDPOINT}"
        response = self._request(url)
        data = response.json()
        modules = data.get("items", [])

        if semester is not None:
            modules = [m for m in modules if m.get("semester") == semester]

        return modules

    def get_module_details(self, scolaryear: int, code: str, instance: str) -> dict:
        """Fetch detailed information for a specific module.

        Args:
            scolaryear: Academic year (e.g., 2024)
            code: Module code (e.g., "G-AIA-400")
            instance: Instance code (e.g., "LYN-4-1")

        Returns:
            Module details including activities
        """
        url = f"{BASE_URL}/module/{scolaryear}/{code}/{instance}/?format=json"
        response = self._request(url)
        return response.json()

    def get_user_info(self) -> UserInfo:
        """Fetch current user profile information.

        Returns:
            UserInfo object with user data
        """
        url = f"{BASE_URL}/user/?format=json"
        response = self._request(url)
        data = response.json()

        gpa_list = data.get("gpa", [])
        gpa = float(gpa_list[0].get("gpa", 0)) if gpa_list else 0.0

        return UserInfo(
            login=data.get("login", ""),
            name=data.get("title", ""),
            semester=data.get("semester", 0),
            student_year=data.get("studentyear", 0),
            promo=data.get("promo", 0),
            credits=data.get("credits", 0),
            gpa=gpa
        )

    def fetch_semester_credits(self, semester: int) -> dict:
        """Fetch credit summary for a semester (quick scan without activities).

        Args:
            semester: Semester number

        Returns:
            Dict with credit counts separated by type:
            - 'pending': Regular module credits (registered, not validated)
            - 'validated': Regular module credits (validated)
            - 'innovation_pending': Innovation (G-INN) credits (registered, not validated)
            - 'innovation_validated': Innovation (G-INN) credits (validated)
        """
        raw_modules = self.get_modules_list(semester)

        # Filter for Lyon campus with credits > 0
        relevant = [
            m for m in raw_modules
            if m.get("instance_location") == "FR/LYN"
            and int(m.get("credits", 0)) > 0
        ]

        pending = 0
        validated = 0
        innovation_pending = 0
        innovation_validated = 0

        for raw in relevant:
            code = raw["code"]
            instance = raw["codeinstance"]
            scolaryear = raw["scolaryear"]
            is_innovation = code.startswith("G-INN")

            try:
                details = self.get_module_details(scolaryear, code, instance)
                registered = details.get("student_registered", 0) == 1
                student_credits = int(details.get("student_credits", 0) or 0)
                module_credits = int(details.get("credits", 0))

                if registered:
                    if student_credits > 0:
                        if is_innovation:
                            innovation_validated += student_credits
                        else:
                            validated += student_credits
                    else:
                        if is_innovation:
                            innovation_pending += module_credits
                        else:
                            pending += module_credits
            except Exception:
                pass

        return {
            "pending": pending,
            "validated": validated,
            "innovation_pending": innovation_pending,
            "innovation_validated": innovation_validated
        }

    def fetch_all_modules(self, semester: int) -> list[Module]:
        """Fetch all modules with their activities for a semester.

        Args:
            semester: Semester number to fetch

        Returns:
            List of Module objects with populated activities
        """
        print(f"Fetching modules for semester {semester}...")

        raw_modules = self.get_modules_list(semester)

        # Filter for Lyon campus with credits > 0
        relevant = [
            m for m in raw_modules
            if m.get("instance_location") == "FR/LYN"
            and int(m.get("credits", 0)) > 0
        ]

        print(f"  {len(relevant)} modules found with credits")

        modules = []
        for i, raw in enumerate(relevant, 1):
            code = raw["code"]
            instance = raw["codeinstance"]
            scolaryear = raw["scolaryear"]

            print(f"  [{i}/{len(relevant)}] {raw['title']}...", end=" ", flush=True)

            try:
                details = self.get_module_details(scolaryear, code, instance)

                activities = []
                for act in details.get("activites", []):
                    begin = parse_date(act.get("begin") or act.get("start"))
                    end = parse_date(act.get("end"))

                    if begin and end:
                        activities.append(Activity(
                            title=act.get("title", ""),
                            type_title=act.get("type_title", ""),
                            begin=begin,
                            end=end,
                            module_title=details.get("title", "")
                        ))

                registered = details.get("student_registered", 0) == 1
                student_credits = int(details.get("student_credits", 0) or 0)

                module = Module(
                    id=raw["id"],
                    code=code,
                    instance=instance,
                    title=details.get("title", raw["title"]),
                    credits=int(details.get("credits", 0)),
                    semester=semester,
                    begin=parse_date(details.get("begin")),
                    end=parse_date(details.get("end")),
                    scolaryear=scolaryear,
                    activities=activities,
                    registered=registered,
                    student_credits=student_credits
                )
                modules.append(module)

                # Show status: registered + pending or validated
                if registered:
                    if student_credits > 0:
                        status = f" [+{student_credits} validated]"
                    else:
                        status = " [pending]"
                else:
                    status = ""
                print(f"OK ({len(activities)} activities){status}")

            except Exception as e:
                print(f"ERROR: {e}")

        return modules
