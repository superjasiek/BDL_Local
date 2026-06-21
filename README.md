# BaDyL - Bank Danych Lokalnych (Local Mirror)

**BaDyL** to narzędzie do tworzenia i utrzymywania lokalnej kopii (mirrora) danych z Głównego Urzędu Statystycznego (GUS) - Banku Danych Lokalnych. Projekt został stworzony z myślą o wydajnym przeglądaniu, wyszukiwaniu i analizowaniu danych statystycznych bezpośrednio na domowym komputerze lub serwerze, bez opóźnień związanych z API i z szerokimi możliwościami filtrowania.

## Zasada działania

1.  **Mirroring danych**: Skrypt `bdl_mirror.py` łączy się z API GUS BDL i pobiera dane dla zdefiniowanych kategorii i zmiennych.
2.  **Efektywność**: Dane są przechowywane lokalnie w bazie SQLite (domyślnie) lub PostgreSQL. Skrypt sprawdza znacznik `lastUpdate` dla każdej zmiennej – jeśli dane w API nie uległy zmianie od ostatniego pobrania, proces jest pomijany, co oszczędza transfer i czas.
3.  **Wyszukiwanie**: Dzięki lokalnej bazie danych, wyszukiwanie wskaźników i jednostek terytorialnych (JST) jest błyskawiczne i pozwala na zaawansowane filtrowanie, którego nie oferuje standardowy interfejs webowy GUS.
4.  **Interfejs użytkownika**: Aplikacja `app.py` zbudowana w Streamlit pozwala na wygodne przeglądanie danych, tworzenie tabel i eksport do formatów CSV/Excel.

## Wymagania

- Python 3.8+
- Biblioteki wymienione w `requirements.txt`
- (Opcjonalnie) Baza danych PostgreSQL

## Instalacja

1.  Sklonuj repozytorium.
2.  Zainstaluj zależności:
    ```bash
    pip install -r requirements.txt
    ```
3.  *(Opcjonalnie)* Skonfiguruj bazę PostgreSQL. Jeśli wolisz SQLite, baza `bdl_mirror.db` zostanie utworzona automatycznie.

## Inicjalizacja i pobieranie danych

### 1. Pobranie jednostek terytorialnych
Na początek należy pobrać strukturę podziału terytorialnego Polski (województwa, powiaty, gminy):
```bash
python3 bdl_mirror.py --units-only
```

### 2. Pobieranie danych tematycznych
Możesz pobrać wszystkie zdefiniowane kategorie lub wybrać konkretną (np. "Struktura demograficzna"):
```bash
python3 bdl_mirror.py --category "Struktura demograficzna"
```
*Domyślnie skrypt pobiera dane z lat 2014-2025.*

### 3. Aktualizacja etykiet użytkownika (dla PostgreSQL)
Jeśli korzystasz z PostgreSQL i interfejsu Streamlit, uruchom:
```bash
python update_user_labels.py
```
Doda to do bazy czytelne nazwy zmiennych zdefiniowane w konfiguracji skryptu.

## Interfejs WWW (Streamlit)

Aby uruchomić aplikację do przeglądania danych:
```bash
streamlit run app.py
```
Interfejs będzie dostępny domyślnie pod adresem `http://localhost:8501`.

## Automatyzacja (Aktualizacje raz w miesiącu)

Dane w BDL są aktualizowane okresowo. Zaleca się uruchamianie skryptu raz w miesiącu za pomocą `cron` (Linux/Raspberry Pi):

```bash
# Otwórz edytor cron
crontab -e

# Dodaj wpis aktualizujący dane 1-go dnia każdego miesiąca o 3:00 rano
0 3 1 * * cd /sciezka/do/projektu && /usr/bin/python3 bdl_mirror.py --year-from $(date +\%Y)
```

## Udostępnianie przez Cloudflare Tunnel

Aby bezpiecznie wystawić BaDyLa do internetu bez otwierania portów na routerze, zaleca się użycie Cloudflare Tunnel.

### Kroki konfiguracji:

1.  **Zainstaluj cloudflared**:
    Pobierz paczkę dla swojego systemu ze strony [Cloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/setup/).
2.  **Zaloguj się**:
    ```bash
    cloudflared tunnel login
    ```
3.  **Utwórz tunel**:
    ```bash
    cloudflared tunnel create badyl-tunnel
    ```
4.  **Skonfiguruj routing**:
    Przypisz tunel do swojej domeny (musisz mieć domenę w Cloudflare):
    ```bash
    cloudflared tunnel route dns badyl-tunnel badyl.twojadomena.pl
    ```
5.  **Uruchom tunel**:
    Skieruj ruch na port Streamlit (8501):
    ```bash
    cloudflared tunnel run --url http://localhost:8501 badyl-tunnel
    ```

Dzięki temu Twoja lokalna instancja BaDyL będzie dostępna pod adresem `https://badyl.twojadomena.pl` z automatycznym certyfikatem SSL.

## Uwagi dot. API GUS
- Skrypt obsługuje rotację kluczy API (do 3 kluczy). Podaj je za pomocą `--api-keys KLUCZ1 KLUCZ2`.
- W przypadku problemów z certyfikatami SSL na starszych systemach, użyj flagi `--no-verify`.
