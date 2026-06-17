import os
import re
import smtplib
import ssl
from email.mime.text import MIMEText
from datetime import datetime

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9",
}

SCRAPERAPI_KEY = os.environ.get("SCRAPERAPI_KEY")  # optional

SHOPS = {
    "ABOUT YOU": {
        "url": "https://www.aboutyou.de/b/shop/sugarshape-193279",
        # Pattern for "# SugarShape\n\n487" style number right before "Ansicht"
        "pattern": r"#\s*SugarShape\s*\n+\s*([\d.]+)\s*\n+\s*Ansicht",
        "render": True,  # JS-Rendering hilfreich/notwendig
    },
    "Zalando": {
        "url": "https://www.zalando.de/damen/sugarshape/",
        "pattern": r"([\d.]+)\s*Artikel",
        "render": False,
    },
    "OTTO": {
        "url": "https://www.otto.de/suche/sugarshape/",
        "pattern": r"([\d.]+)\s*Produkte",
        "render": False,
    },
}


def fetch_html(url, render=False):
    """Holt HTML, nutzt ScraperAPI falls Key gesetzt ist (umgeht Bot-Schutz),
    sonst direkten Request mit Browser-Headern."""
    if SCRAPERAPI_KEY:
        params = {
            "api_key": SCRAPERAPI_KEY,
            "url": url,
            "country_code": "de",
        }
        if render:
            params["render"] = "true"
        resp = requests.get(
            "https://api.scraperapi.com/", params=params, timeout=70
        )
        resp.raise_for_status()
        return resp.text
    else:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return resp.text


def fetch_count(name, cfg):
    try:
        html = fetch_html(cfg["url"], render=cfg.get("render", False))
        match = re.search(cfg["pattern"], html)
        if match:
            number_str = match.group(1).replace(".", "")
            return int(number_str)
        return None
    except Exception as e:
        print(f"Fehler bei {name}: {e}")
        return None


def send_email(results):
    sender = os.environ["EMAIL_SENDER"]
    password = os.environ["EMAIL_PASSWORD"]
    recipient = os.environ["EMAIL_RECIPIENT"]

    today = datetime.now().strftime("%d.%m.%Y")

    lines = [f"SugarShape Artikelanzahl - {today}", ""]
    for shop, count in results.items():
        display = count if count is not None else "FEHLER / nicht gefunden"
        lines.append(f"{shop}: {display}")

    body = "\n".join(lines)

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"SugarShape Report - {today}"
    msg["From"] = sender
    msg["To"] = recipient

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())


def main():
    results = {}
    for name, cfg in SHOPS.items():
        results[name] = fetch_count(name, cfg)
        print(f"{name}: {results[name]}")

    send_email(results)
    print("E-Mail gesendet.")


if __name__ == "__main__":
    main()
