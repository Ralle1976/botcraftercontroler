
# BotCrafterController

BotCrafterController ist eine Flask-basierte Webanwendung, die die Google Drive API und die GitHub API vollständig integriert. Die Anwendung bietet Endpunkte zur Verwaltung von Dateien in Google Drive sowie zur Interaktion mit GitHub-Repositories.

---

## **Features**

### Google Drive API
- **Datei hochladen**: Lädt eine Datei in Google Drive hoch.
- **Dateien auflisten**: Listet Dateien in einem Ordner oder im gesamten Google Drive auf.
- **Datei herunterladen**: Lädt eine Datei basierend auf der `file_id` herunter.
- **Datei löschen**: Löscht eine Datei basierend auf der `file_id`.
- **Ordner erstellen**: Erstellt einen neuen Ordner.

### GitHub API
- **Repository erstellen**: Erstellt ein neues GitHub-Repository.
- **Dateien auflisten**: Listet Dateien in einem Repository-Verzeichnis auf.
- **Datei hochladen/aktualisieren**: Lädt eine Datei hoch oder aktualisiert sie.
- **Datei löschen**: Löscht eine Datei aus einem Repository.
- **Branch erstellen**: Erstellt einen neuen Branch.
- **Pull Request erstellen**: Erstellt einen Pull Request.

---

## **Installation**

### Voraussetzungen
1. **Python 3.10 oder höher**
2. **Abhängigkeiten in `requirements.txt`**

### Lokale Installation
1. Repository klonen:
    ```bash
    git clone https://github.com/<your-username>/<your-repository>.git
    cd <your-repository>
    ```

2. Virtuelle Umgebung erstellen und aktivieren:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Für Unix/Mac
    venv\Scripts\activate  # Für Windows
    ```

3. Abhängigkeiten installieren:
    ```bash
    pip install -r requirements.txt
    ```

4. Anwendung starten:
    ```bash
    python run.py
    ```

Die Anwendung läuft unter `http://127.0.0.1:5000`.

---

## **Umgebungsvariablen**

Die Anwendung verwendet folgende Umgebungsvariablen:
- `GOOGLE_CREDENTIALS`: JSON-Inhalt der Google Service Account Credentials.
- `GITHUB_TOKEN`: Personal Access Token für die GitHub API.
- `SECRET_KEY`: Flask-Anwendungsschlüssel.

### Beispiel: Google Credentials setzen
Falls `credentials.json` lokal vorhanden ist:
```bash
export GOOGLE_CREDENTIALS="$(cat credentials.json)"
```

---

## **Bereitstellung auf Heroku**

1. Anwendung zu Heroku pushen:
    ```bash
    git push heroku main
    ```

2. Umgebungsvariablen konfigurieren:
    ```bash
    heroku config:set GOOGLE_CREDENTIALS="$(cat credentials.json)"
    heroku config:set GITHUB_TOKEN="<your_github_token>"
    ```

3. Logs überprüfen:
    ```bash
    heroku logs --tail
    ```

---

## **API-Endpunkte**

### **Google Drive API**
1. **Dateien auflisten**
    - **GET** `/list-files`
    - Query-Parameter: `folder_id` (optional)
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

### **GitHub API**
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
    - **GET** `/list-files`
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

## **Beispiel für Umgebungsvariablen**
Erstelle eine `.env`-Datei (optional für lokale Entwicklung):
```
GOOGLE_CREDENTIALS={"type": "service_account", ...}
GITHUB_TOKEN=your_github_token
SECRET_KEY=your_secret_key
```

---

## **Tests**

### Lokale Tests
- Stelle sicher, dass `GOOGLE_CREDENTIALS` und `GITHUB_TOKEN` gesetzt sind.
- Starte die Tests:
    ```bash
    pytest
    ```

---

## **Lizenz**

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).
