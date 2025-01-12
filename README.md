
# BotCrafterController

BotCrafterController ist eine Flask-basierte Anwendung, die eine umfassende Integration der Google Drive API und der GitHub API bietet. 
Die App ermöglicht die Verwaltung von Dateien in Google Drive sowie die Interaktion mit GitHub-Repositories.

---

## **Features**

### Google Drive API
- Hochladen von Dateien in Google Drive.
- Auflisten von Dateien und Ordnern.
- Herunterladen von Dateien.
- Löschen von Dateien.
- Erstellen von Ordnern.

### GitHub API
- Erstellung neuer Repositories.
- Auflisten von Dateien in einem Repository.
- Hochladen und Aktualisieren von Dateien in einem Repository.
- Löschen von Dateien in einem Repository.
- Erstellung neuer Branches.
- Erstellung von Pull Requests.

---

## **Architekturübersicht**

Die Anwendung ist modular aufgebaut:
- `app/` - Hauptverzeichnis der Anwendung.
  - `__init__.py` - Initialisierung der Flask-App.
  - `routes.py` - Definition der API-Endpunkte.
  - `github_api.py` - Funktionen für die GitHub API.
  - `gdrive_api.py` - Funktionen für die Google Drive API.
- `config.py` - Konfigurationsklasse für Umgebungsvariablen.
- `run.py` - Startpunkt der Anwendung.
- `requirements.txt` - Liste der Python-Abhängigkeiten.
- `Procfile` - Heroku-Konfigurationsdatei.

---

## **Installation**

### Voraussetzungen
- **Python 3.10 oder höher**
- **Abhängigkeiten** in `requirements.txt`.

### Schritte
1. **Repository klonen**:
    ```bash
    git clone https://github.com/<your-username>/<your-repository>.git
    cd <your-repository>
    ```

2. **Virtuelle Umgebung erstellen und aktivieren**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Für Unix/Mac
    venv\Scripts\activate  # Für Windows
    ```

3. **Abhängigkeiten installieren**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Anwendung starten**:
    ```bash
    python run.py
    ```

Die Anwendung ist jetzt unter `http://127.0.0.1:5000` verfügbar.

---

## **Konfiguration**

Die Anwendung verwendet folgende Umgebungsvariablen:
- `GOOGLE_CREDENTIALS`: JSON-Inhalt der Google Service Account Credentials.
- `GITHUB_REPO_CONFIG`: JSON-Inhalt mit Repositories und zugehörigen Tokens.
- `SECRET_KEY`: Flask-Secret-Key.

### Beispielkonfiguration für `GITHUB_REPO_CONFIG`:
```json
{
    "repo1": {
        "url": "https://github.com/Ralle1976/botcrafter",
        "token": "MeinToken1"
    },
    "repo2": {
        "url": "https://github.com/Ralle1976/botcraftercontroler",
        "token": "MeinToken2"
    }
}
```

### Setzen der Umgebungsvariablen auf Heroku:
```bash
heroku config:set GOOGLE_CREDENTIALS="$(cat credentials.json)"
heroku config:set GITHUB_REPO_CONFIG='{
    "repo1": {
        "url": "https://github.com/Ralle1976/botcrafter",
        "token": "MeinToken1"
    },
    "repo2": {
        "url": "https://github.com/Ralle1976/botcraftercontroler",
        "token": "MeinToken2"
    }
}'
```

---

## **API-Endpunkte**

### Google Drive API
1. **Dateien auflisten**
    - **GET** `/list-files`
    - Query-Parameter: `folder_id` (optional).
    - Beispiel:
        ```bash
        curl -X GET "http://127.0.0.1:5000/list-files?folder_id=<FOLDER_ID>"
        ```

2. **Datei hochladen**
    - **POST** `/upload-file`
    - Body (JSON):
        ```json
        {
            "file_path": "path/to/file",
            "mime_type": "text/plain",
            "parent_folder_id": "optional-folder-id"
        }
        ```

3. **Datei löschen**
    - **DELETE** `/delete-file`
    - Body (JSON):
        ```json
        {
            "file_id": "file-id"
        }
        ```

### GitHub API
1. **Repository erstellen**
    - **POST** `/create-repo`
    - Body (JSON):
        ```json
        {
            "repo_name": "my-new-repo",
            "private": true
        }
        ```

2. **Dateien auflisten**
    - **GET** `/list-repo-files`
    - Query-Parameter:
        - `owner`: Repository-Besitzer.
        - `repo`: Repository-Name.
        - `path` (optional): Pfad innerhalb des Repositories.

3. **Pull Request erstellen**
    - **POST** `/create-pull-request`
    - Body (JSON):
        ```json
        {
            "title": "Update ReadMe",
            "head": "branch-name",
            "base": "main"
        }
        ```

---

## **OpenAPI Schema**

Ein vollständiges Schema für die API befindet sich in der Datei [openapi_complete.yaml](openapi_complete.yaml). Es deckt alle Endpunkte und ihre Details ab.

---

## **Tests**

### Lokale Tests ausführen:
```bash
pytest
```

---

## **Bekannte Probleme**
- **API-Schlüssel sichern:** Stelle sicher, dass Tokens niemals in der API-Rückgabe oder in Logs erscheinen.
- **Fehler bei Google Drive API:** Vergewissere dich, dass die JSON-Credentials korrekt gesetzt sind.

---

## **Support**
Bei Fragen oder Problemen erreichst du uns unter `Ralf.Arnold@it-bfw.de`.

---

## **Lizenz**
Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).
