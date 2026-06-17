# SugarShape Daily Report – Einrichtung

Dieser Agent prüft täglich um 08:00 Uhr (Berlin-Zeit) die Anzahl der SugarShape-Artikel
bei ABOUT YOU, Zalando und OTTO und sendet dir das Ergebnis per E-Mail.

## 1. GitHub-Repository erstellen

1. Erstelle ein neues (privates) GitHub-Repository, z. B. `sugarshape-monitor`.
2. Lade diese beiden Dateien ins Repository hoch (Ordnerstruktur beibehalten):
   - `check_sugarshape.py`
   - `.github/workflows/daily-report.yml`

## 2. ScraperAPI-Account einrichten (umgeht Bot-Schutz)

ABOUT YOU, Zalando und OTTO blockieren einfache automatisierte Requests
(HTTP 403). Damit der Agent trotzdem zuverlässig funktioniert, nutzt das
Skript optional ScraperAPI als Proxy:

1. Registriere dich kostenlos auf https://www.scraperapi.com/
   (Free-Tier: 1.000 Requests/Monat – für 1x täglich 3 Requests reichen
   ca. 90/Monat aus).
2. Kopiere deinen API-Key aus dem Dashboard.

Falls du keinen ScraperAPI-Key hinterlegst, versucht das Skript einen
direkten Request mit Browser-Headern. Das kann bei diesen Shops trotzdem
mit "FEHLER / nicht gefunden" enden.

## 3. Gmail-App-Passwort erstellen (für den E-Mail-Versand)

Da Gmail normale Passwörter für SMTP nicht mehr akzeptiert, brauchst du ein
"App-Passwort":

1. Aktiviere die 2-Faktor-Authentifizierung für dein Google-Konto (falls noch nicht aktiv):
   https://myaccount.google.com/security
2. Gehe zu: https://myaccount.google.com/apppasswords
3. Erstelle ein neues App-Passwort (z. B. Name "SugarShape Report").
4. Kopiere das 16-stellige Passwort – das brauchst du im nächsten Schritt.

(Alternativ kannst du auch einen anderen SMTP-Anbieter nutzen – dann im Skript
`smtp.gmail.com` und Port anpassen.)

## 4. Secrets in GitHub hinterlegen

Im Repository:
`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

Lege folgende Secrets an:

| Name              | Wert                                              |
|-------------------|---------------------------------------------------|
| EMAIL_SENDER      | deine-gmail-adresse@gmail.com                     |
| EMAIL_PASSWORD    | das 16-stellige App-Passwort aus Schritt 3        | udct ygqe mmsr zuml
| EMAIL_RECIPIENT   | E-Mail-Adresse, an die der Report gehen soll      |
| SCRAPERAPI_KEY    | dein API-Key aus Schritt 2 (optional, aber empfohlen) | 32e2983d3f1d6bab825efc93dc843a45

(EMAIL_SENDER und EMAIL_RECIPIENT können identisch sein, wenn du dir die Mail
selbst schicken willst.)

## 5. Fertig

Der Workflow läuft automatisch jeden Tag um 06:00 UTC (= 08:00 Uhr Berlin-Zeit
in der Sommerzeit / 07:00 Uhr in der Winterzeit). GitHub Actions ist für
öffentliche und private Repos im normalen Umfang kostenlos.

## 6. Manuell testen

Im Reiter "Actions" des Repos kannst du den Workflow "SugarShape Daily Report"
auswählen und über "Run workflow" sofort manuell ausführen, um zu prüfen, ob
alles funktioniert.

## Hinweise zum Bot-Schutz

ABOUT YOU, Zalando und OTTO setzen Bot-Schutz (Cloudflare/Akamai o. ä.) ein.
Mit ScraperAPI sollte der Zugriff in den meisten Fällen funktionieren – bei
ABOUT YOU ist zusätzlich `render: true` aktiviert (JavaScript-Rendering),
da die Artikelanzahl dort vermutlich erst per JS nachgeladen wird. Das
verbraucht pro Request mehr "API-Credits" bei ScraperAPI (zählt oft als
mehrere Requests), ist im Free-Tier für 1x täglich aber unproblematisch.

Sollte ein Shop dennoch "FEHLER / nicht gefunden" liefern:
- Prüfe in den Action-Logs die Fehlermeldung.
- Prüfe, ob sich das Seitenlayout geändert hat und passe das Regex-Pattern
  in `check_sugarshape.py` (Variable `SHOPS`) an.
- Ggf. bei ABOUT YOU auch ohne `render: true` testen oder umgekehrt bei den
  anderen Shops `render: true` aktivieren.

## Allgemeine Hinweise

- Die Skripte parsen die Artikelanzahl aus dem HTML der jeweiligen Shop-Seiten
  via Regex. Wenn die Shops ihr Seitenlayout ändern, muss das passende
  Regex-Pattern in `check_sugarshape.py` (Variable `SHOPS`) angepasst werden.
