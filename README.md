# Gladius – Desktop-App

Indoor-Cycling-Training für Windows mit transparentem HUD über jedem anderen Fenster (YouTube, Netflix, Browser im Vollbild …).

## Einmalig: Node.js installieren
1. https://nodejs.org öffnen und die **LTS-Version** für Windows installieren (Standard-Einstellungen genügen).
2. Danach ist der Befehl `npm` verfügbar.

## Gladius starten
1. Den Ordner `gladius-desktop` entpacken, z. B. nach `C:\Users\<du>\gladius-desktop`.
2. Im Ordner in die Adresszeile des Explorers `cmd` tippen und Enter drücken – ein Terminal öffnet sich direkt in diesem Ordner.
3. Einmalig: `npm install` (lädt Electron, dauert 1–2 Minuten)
4. Starten: `npm start`

## Als richtiges Programm installieren (optional)
`npm run dist` erzeugt im Ordner `dist` ein Installationsprogramm **Gladius Setup x.y.z.exe**.
Danach startest du Gladius wie jedes andere Programm über das Startmenü – ohne Terminal.
Windows zeigt beim ersten Start evtl. „Der Computer wurde durch Windows geschützt“, weil das Programm nicht signiert ist: *Weitere Informationen → Trotzdem ausführen*.

## Das HUD
- **„◩ HUD einblenden“** im Training oder **Ctrl+Alt+H** (funktioniert überall).
- Das HUD ist durchsichtig, liegt über allen Fenstern und lässt alle Klicks durch – du bedienst YouTube ganz normal.
- Es erscheint auf dem Bildschirm, auf dem gerade die Maus ist.
- Grösse und Deckkraft: ⚙ Einstellungen → HUD-Grösse / HUD-Deckkraft.
- ▲ neben der Leistung = mehr treten, ▼ = weniger.

## Tastenkürzel (überall, auch wenn YouTube im Vordergrund ist)
| Kürzel | Funktion |
|---|---|
| Ctrl+Alt+H | HUD ein/aus |
| Ctrl+Shift+↑ / ↓ | Hochschalten / Runterschalten |
| Ctrl+Alt+P | Pause / Weiter |
| Ctrl+Alt+N | Nächstes Intervall |

## Zwift Click (v1 und v2)
- In der Kopfzeile **„Click verbinden“**. Der Click v2 hat zwei Pods: am Pod kurz eine Taste drücken, dann verbinden – für den zweiten Pod nochmals.
- Standard: **+** = Hochschalten, **−** = Runterschalten (gedrückt halten = mehrere Gänge).
- ⚙ Einstellungen → **Tastenbelegungen**: jede Taste (Schalttasten, Steuerkreuz, A/B/Y/Z) frei belegen – Training (Pause, nächstes Intervall, Intensität, HUD …) oder **Multimedia** (Wiedergabe/Pause, Titel, Lautstärke für YouTube, Spotify & Co.).
- Zwift, MyWhoosh und die Companion-App vorher schliessen: der Click nimmt nur eine Verbindung an.

## Gut zu wissen
- Bluetooth: Beim Verbinden zeigt Gladius eine eigene Geräteliste. Trainer antreten bzw. Pulsgurt anlegen, damit sie auftauchen.
  MyWhoosh/Zwift vorher schliessen – der Trainer verbindet sich nur mit einer App.
- Während einer Fahrt geht der Bildschirm nicht in den Ruhezustand.
- Gladius läuft ungebremst weiter, auch wenn das Fenster minimiert oder verdeckt ist.
- Die Desktop-App hat einen **eigenen Datenspeicher** – Fahrten aus der Browser-Version werden nicht übernommen.
- Spiele im *exklusiven* Vollbildmodus können Overlays verdecken; Videos im Browser-Vollbild sind kein Problem.
