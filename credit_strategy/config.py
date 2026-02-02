"""Configuration constants for the Credit Strategy tool."""

BASE_URL = "https://intra.epitech.eu"

MODULES_ENDPOINT = (
    "/course/filter?format=json&preload=1"
    "&location%5B%5D=FR&location%5B%5D=FR%2FLYN"
    "&course%5B%5D=bachelor%2Fclassic"
    "&scolaryear%5B%5D=2024&scolaryear%5B%5D=2025"
)

# Module categories with their display name and color
MODULE_CATEGORIES = {
    "G-AIA": ("AI & Machine Learning", "C6EFCE"),
    "G-SEC": ("Security", "F8CBAD"),
    "G-OOP": ("Object-Oriented Programming", "BDD7EE"),
    "G-NWP": ("Network Programming", "FFE699"),
    "G-CCP": ("Concurrent Programming", "E2EFDA"),
    "G-DOP": ("DevOps", "D9E1F2"),
    "G-CNA": ("Computer Numerical Analysis", "FCE4D6"),
    "G-ING": ("Engineering", "DDEBF7"),
    "G-PMP": ("Project Management", "FFF2CC"),
    "G-PRO": ("Professional", "E2F0D9"),
    "G-ENG": ("English", "F2F2F2"),
    "G-YEP": ("Year-End Project", "FF9999"),
    "G-INN": ("Innovation", "DDA0DD"),
    "G-CUS": ("Customer/UX", "FFFACD"),
    "G-EPI": ("Epitech Life", "D3D3D3"),
    "G-PDG": ("Paradigms", "B0E0E6"),
}

# Pastel color palette for module timeline bars
MODULE_COLORS = [
    "A8D5BA",  # Sage green
    "B5D8EB",  # Sky blue
    "F7DC6F",  # Soft yellow
    "F1948A",  # Coral red
    "D7BDE2",  # Lavender
    "A9CCE3",  # Powder blue
    "F5CBA7",  # Peach
    "A3E4D7",  # Pale turquoise
    "FAD7A0",  # Apricot
    "D5DBDB",  # Pearl gray
    "ABEBC6",  # Mint
    "F9E79F",  # Pale yellow
    "D2B4DE",  # Pale purple
    "AED6F1",  # Baby blue
    "F5B7B1",  # Dusty pink
    "A9DFBF",  # Sea green
    "FADBD8",  # Salmon pink
    "D4E6F1",  # Glacier blue
    "FCF3CF",  # Cream
    "E8DAEF",  # Lilac
]

# HTTP headers to simulate browser AJAX requests
REQUEST_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    ),
    "Referer": "https://intra.epitech.eu/module/",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Ch-Ua": '"Not(A:Brand";v="8", "Chromium";v="144"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}
