# BaDyL - Bank Danych Lokalnych (Local Mirror)

**BaDyL** to narzędzie do tworzenia i utrzymywania lokalnej kopii (mirrora) danych z Głównego Urzędu Statystycznego (GUS) - Banku Danych Lokalnych. Projekt został stworzony z myślą o wydajnym przeglądaniu, wyszukiwaniu i analizowaniu danych statystycznych bezpośrednio na domowym komputerze lub serwerze, bez opóźnień związanych z API i z szerokimi możliwościami filtrowania.

## Zasada działania

1.  **Mirroring danych**: Skrypt `bdl_mirror.py` łączy się z API GUS BDL i pobiera dane dla zdefiniowanych kategorii i zmiennych.
2.  **Baza danych**: Podstawowym silnikiem bazy danych jest **PostgreSQL**, który zapewnia wydajność przy dużych zbiorach danych i pełną obsługę interfejsu graficznego. (Opcjonalnie wspierany jest również SQLite dla mniejszych wdrożeń).
3.  **Wyszukiwanie**: Dzięki lokalnej bazie danych, wyszukiwanie wskaźników i jednostek terytorialnych (JST) jest błyskawiczne i pozwala na zaawansowane filtrowanie, którego nie oferuje standardowy interfejs webowy GUS.
4.  **Interfejs graficzny (GUI)**: Głównym sposobem interakcji z danymi jest aplikacja oparta na **Streamlit** (`app.py`). Pozwala ona na wygodne przeglądanie danych, tworzenie tabel i eksport do formatów CSV/Excel.

## Wymagania

- Python 3.8+
- **PostgreSQL** (zalecana i podstawowa baza danych)
- Biblioteki wymienione w `requirements.txt`

## Instalacja i Konfiguracja

1.  Sklonuj repozytorium.
2.  Zainstaluj zależności:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Konfiguracja połączenia**: Przed uruchomieniem należy ustawić parametry połączenia z bazą PostgreSQL (tzw. DSN) w plikach:
    - `app.py` (zmienna `DSN`)
    - `update_user_labels.py` (zmienna `DSN`)
    - Podczas uruchamiania `bdl_mirror.py` parametry podaje się w argumencie `--pg-dsn`.

## Inicjalizacja i pobieranie danych

### 1. Pobranie jednostek terytorialnych
Na początek należy pobrać strukturę podziału terytorialnego Polski (województwa, powiaty, gminy):
```bash
python3 bdl_mirror.py --db-type postgres --pg-dsn "Twoj_DSN" --units-only
```

### 2. Pobieranie danych tematycznych
Pobierz dane dla wybranych kategorii:
```bash
python3 bdl_mirror.py --db-type postgres --pg-dsn "Twoj_DSN" --category "Struktura demograficzna"
```
*Domyślnie skrypt pobiera dane z lat 2014-2025.*

### 3. Aktualizacja etykiet (Kluczowe dla GUI)
Aby interfejs graficzny poprawnie wyświetlał nazwy wskaźników, należy uruchomić skrypt aktualizujący etykiety:
```bash
python3 update_user_labels.py
```

## Obsługa Interfejsu Graficznego (Streamlit)

Za warstwę wizualną projektu odpowiada plik **`app.py`**. Aby go uruchomić:
```bash
streamlit run app.py
```
Po uruchomieniu interfejs będzie dostępny pod adresem `http://localhost:8501`.

## Automatyzacja (Aktualizacje raz w miesiącu)

Dane w BDL są aktualizowane okresowo. Zaleca się uruchamianie synchronizacji raz w miesiącu za pomocą `cron`:

```bash
# Dodaj wpis aktualizujący dane 1-go dnia każdego miesiąca o 3:00 rano
0 3 1 * * cd /sciezka/do/projektu && /usr/bin/python3 bdl_mirror.py --db-type postgres --pg-dsn "Twoj_DSN" --year-from $(date +\%Y)
```

## Udostępnianie przez Cloudflare Tunnel

Aby bezpiecznie wystawić interfejs BaDyLa do internetu:

1.  **Zaloguj się**: `cloudflared tunnel login`
2.  **Utwórz tunel**: `cloudflared tunnel create badyl-tunnel`
3.  **Skonfiguruj routing**: `cloudflared tunnel route dns badyl-tunnel badyl.twojadomena.pl`
4.  **Uruchom tunel** (przekierowanie na port Streamlit):
    ```bash
    cloudflared tunnel run --url http://localhost:8501 badyl-tunnel
    ```

## Uwagi dot. API GUS
- Skrypt obsługuje rotację kluczy API (do 3 kluczy). Podaj je za pomocą `--api-keys KLUCZ1 KLUCZ2`.
- W przypadku problemów z certyfikatami SSL na starszych systemach (np. Raspberry Pi), użyj flagi `--no-verify`.
