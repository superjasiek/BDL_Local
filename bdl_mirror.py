import sqlite3
import requests
import time
import sys
import os

BASE_URL = "https://bdl.stat.gov.pl/api/v1"
DB_NAME = "bdl_mirror.db"

API_KEYS = []
current_key_index = 0

# Variables provided by the user
VARIABLES_MAP = {
    "Struktura demograficzna": [
        (72305, "Ludność ogółem do przeliczeń"),
        (60567, "Udział ludności wg ekonomicznych grup wieku w % ludności ogółem wiek przedprodukcyjny"),
        (60566, "Udział ludności wg ekonomicznych grup wieku w % ludności ogółem wiek produkcyjny"),
        (60565, "Udział ludności wg ekonomicznych grup wieku w % ludności ogółem wiek wiek poprodukcyjny"),
        (634989, "Odsetek osób w wieku 65 lat i więcej w populacji ogółem"),
        (60563, "Ludność w wieku nieprodukcyjnym na 100 osób w wieku produkcyjnym"),
        (60559, "ludność na 1km2"),
        (72306, "Ludność wg grup wieku i płci 0-4 ogółem"),
        (72307, "Ludność wg grup wieku i płci 5-9 ogółem"),
        (72308, "Ludność wg grup wieku i płci 10-14 ogółem"),
        (72309, "Ludność wg grup wieku i płci 15-19 ogółem"),
        (47734, "Ludność wg grup wieku i płci 20-24 ogółem"),
        (47694, "Ludność wg grup wieku i płci 25-29 ogółem"),
        (47722, "Ludność wg grup wieku i płci 30-34 ogółem"),
        (47701, "Ludność wg grup wieku i płci 35-39 ogółem"),
        (47707, "Ludność wg grup wieku i płci 40-44 ogółem"),
        (47726, "Ludność wg grup wieku i płci 45-49 ogółem"),
        (47717, "Ludność wg grup wieku i płci 50-54 ogółem"),
        (47732, "Ludność wg grup wieku i płci 55-59 ogółem"),
        (47739, "Ludność wg grup wieku i płci 60-64 ogółem"),
        (72239, "Ludność wg grup wieku i płci 65-69 ogółem"),
        (72240, "Ludność wg grup wieku i płci 70 i więcej ogółem"),
        (76022, "Ludność wg grup wieku i płci 70-74 ogółem"),
        (76023, "Ludność wg grup wieku i płci 75-79 ogółem"),
        (76024, "Ludność wg grup wieku i płci 80-84 ogółem"),
        (76025, "Ludność wg grup wieku i płci 85 i więcej ogółem"),
        (454048, "Ludność wg grup wieku i płci 0-14 ogółem"),
        (72301, "Ludność wg grup wieku i płci 0-4 mężczyźni"),
        (72302, "Ludność wg grup wieku i płci 5-9 mężczyźni"),
        (72303, "Ludność wg grup wieku i płci 10-14 mężczyźni"),
        (72304, "Ludność wg grup wieku i płci 15-19 mężczyźni"),
        (47711, "Ludność wg grup wieku i płci 20-24 mężczyźni"),
        (47736, "Ludność wg grup wieku i płci 25-29 mężczyźni"),
        (47724, "Ludność wg grup wieku i płci 30-34 mężczyźni"),
        (47712, "Ludność wg grup wieku i płci 35-39 mężczyźni"),
        (47725, "Ludność wg grup wieku i płci 40-44 mężczyźni"),
        (47728, "Ludność wg grup wieku i płci 45-49 mężczyźni"),
        (47706, "Ludność wg grup wieku i płci 50-54 mężczyźni"),
        (47715, "Ludność wg grup wieku i płci 55-59 mężczyźni"),
        (47721, "Ludność wg grup wieku i płci 60-64 mężczyźni"),
        (72243, "Ludność wg grup wieku i płci 65-69 mężczyźni"),
        (72238, "Ludność wg grup wieku i płci 70 i więcej mężczyźni"),
        (76018, "Ludność wg grup wieku i płci 70-74 mężczyźni"),
        (76019, "Ludność wg grup wieku i płci 75-79 mężczyźni"),
        (76020, "Ludność wg grup wieku i płci 80-84 mężczyźni"),
        (76021, "Ludność wg grup wieku i płci 85 i więcej mężczyźni"),
        (454047, "Ludność wg grup wieku i płci 0-14 mężczyźni"),
        (72296, "Ludność wg grup wieku i płci 0-4 kobiety"),
        (72297, "Ludność wg grup wieku i płci 5-9 kobiety"),
        (72298, "Ludność wg grup wieku i płci 10-14 kobiety"),
        (72299, "Ludność wg grup wieku i płci 15-19 kobiety"),
        (47738, "Ludność wg grup wieku i płci 20-24 kobiety"),
        (47696, "Ludność wg grup wieku i płci 25-29 kobiety"),
        (47695, "Ludność wg grup wieku i płci 30-34 kobiety"),
        (47716, "Ludność wg grup wieku i płci 35-39 kobiety"),
        (47698, "Ludność wg grup wieku i płci 40-44 kobiety"),
        (47727, "Ludność wg grup wieku i płci 45-49 kobiety"),
        (47723, "Ludność wg grup wieku i płci 50-54 kobiety"),
        (47702, "Ludność wg grup wieku i płci 55-59 kobiety"),
        (47693, "Ludność wg grup wieku i płci 60-64 kobiety"),
        (72241, "Ludność wg grup wieku i płci 65-69 kobiety"),
        (72242, "Ludność wg grup wieku i płci 70 i więcej kobiety"),
        (76014, "Ludność wg grup wieku i płci 70-74 kobiety"),
        (76015, "Ludność wg grup wieku i płci 75-79 kobiety"),
        (76016, "Ludność wg grup wieku i płci 80-84 kobiety"),
        (76017, "Ludność wg grup wieku i płci 85 i więcej kobiety"),
        (454046, "Ludność wg grup wieku i płci 0-14 kobiety"),
        (149, "Ludność w wieku przedprodukcyjnym"),
        (152, "Ludność w wieku produkcyjnym"),
        (155, "Ludność w wieku poprodukcyjnym"),
    ],
    "Ruch ludności": [
        (450551, "Przyrost naturalny na 1000 ludności"),
        (453193, "Saldo migracji na 1000 ludności"),
        (450540, "Urodzenia żywe na 1000 ludności (współczynnik urodzeń)"),
        (450541, "Zgony na 1000 ludności (współczynnik zgonów)"),
        (149160, "Wymeldowania ogółem"),
        (149156, "Zameldowania ogółem"),
        (149164, "Saldo migracji"),
        (149157, "Zameldowania z miast"),
        (149158, "Zameldowania ze wsi"),
        (149161, "Wymeldowania do miast"),
        (149162, "Wymeldowania na wieś"),
        (59, "Urodzenia ogółem"),
        (65, "Zgodny ogółem"),
        (68, "Przyrost naturalny"),
    ],
    "Kapitał społeczny": [
        (474461, "Frekwencja wyborcza sejmiki województw"),
        (474460, "Frekwencja wyborcza rady powiatów"),
        (474463, "Frekwencja wyborcza rady gmin i rady miast w miastach na prawach powiatu"),
        (474462, "Frekwencja wyborcza wójtowie, burmistrzowie i prezydenci miast"),
        (454061, "Fundacje, stowarzyszenia i organizacje społeczne na 1000 ludności"),
        (152714, "Wybrane podmioty wg sektorów własnościowych fundacje"),
        (152715, "Wybrane podmioty wg sektorów własnościowych stowarzyszenia i organizacje społeczne"),
    ],
    "Edukacja": [
        (1617169, "Odsetek dzieci w wieku 3-6 lat objętych wychowaniem przedszkolnym"),
        (60258, "Współczynnik skolaryzacji brutto - szkoły podstawowe"),
        (1617119, "Dzieci w wieku przedszkolnym 3-6 lat"),
        (1617144, "Dzieci objęte wychowaniem przedszkolnym 3-6 lat"),
        (410639, "Dzieci w wieku do 3 lat ogółem"),
        (151867, "Uczniowie szkół podstawowych"),
        (455392, "Uczniowie szkół ponadpodstawowych ogólnokształcących"),
        (455403, "Uczniowie szkół ponadpodstawowych technika"),
        (569055, "Uczniowie szkół ponadpodstawowych branżowych"),
    ],
    "Kultura": [
        (60191, "Czytelnicy bibliotek publicznych na 1000 ludności"),
        (60188, "wypożyczenia księgozbioru na 1 czytelnika w woluminach"),
        (60189, "księgozbiór bibliotek na 1000 ludności"),
        (1539661, "zwiedzający muzea i oddziały na 1000 ludności"),
        (265989, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja R dział 90"),
        (58505, "Imprezy organizowane przez centra, domy i ośrodki kultury, kluby i świetlice"),
        (58506, "Uczestnicy imprez organizowanych przez centra, domy i ośrodki kultury, kluby i świetlice"),
        (58509, "Liczba kół, klubów i sekcji"),
        (58510, "Członkowie kół, klubów i sekcji"),
        (58511, "Grupy artystyczne"),
        (58507, "Członkowie grup artystycznych"),
        (35719, "biblioteki czytelnicy"),
        (35715, "biblioteki wypożyczenia księgozbioru na zewnątrz"),
        (1243, "zwiedzający muzea i oddziały"),
    ],
    "Pomoc społeczna": [
        (410641, "Odsetek dzieci objętych opieką w żłobkach"),
        (1649859, "Dzieci w żłobkach i klubach dziecięcych na 1000 dzieci w wieku do lat 3"),
        (1649860, "Miejsca w żłobkach i klubach dziecięcych na 1000 dzieci w wieku do lat 3"),
        (1548717, "Beneficjenci środowiskowej pomocy społecznej na 10 tys. ludności"),
        (410640, "Dzieci objęte opieką w żłobkach"),
        (259886, "rodziny otrzymujące zasiłki rodzinne na dzieci"),
        (259888, "dzieci w wieku do lat 17, na które rodzice otrzymują zasiłek rodzinny"),
    ],
    "Ochrona zdrowia": [
        (60583, "ludność na aptekę ogólnodostępną"),
        (1616687, "Porady lekarskie ogółem"),
        (266458, "Liczba podmiotów gospodarczych prowadzących działalność w sektorze opieka zdrowotna (PKD: Sekcja Q - 86)"),
        (194884, "Liczba aptek"),
    ],
    "Mieszkalnictwo": [
        (410600, "Mieszkania na 1000 ludności"),
        (60573, "Przeciętna powierzchnia użytkowa mieszkania na 1 osobę"),
        (396046, "Udział powierzchni objętej obowiązującymi miejscowymi planami zagospodarowania przestrzennego w powierzchni ogółem"),
        (747060, "mieszkania oddane do użytkowania na 1000 ludności"),
        (60811, "Liczba mieszkań"),
        (1641257, "pozwolenia i zgłoszenia z projektem, nowe budynki mieszkalne jednorodzinne (jednomieszkaniowe)"),
        (1641256, "pozwolenia i zgłoszenia z projektem, budynki ogółem"),
        (748601, "mieszkania oddane do użytkowania ogółem"),
        (199955, "mieszkania komunalne, mieszkania ogółem"),
        (199953, "mieszkania komunalne, powierzchnia użytkowa"),
    ],
    "Przedsiębiorczość": [
        (265726, "Podmioty ogółem do przeliczeń"),
        (60530, "Podmioty wpisane do rejestru REGON na 10 tys. ludności"),
        (1548701, "Osoby fizyczne prowadzące działalność gospodarczą na 10 tys. ludności"),
        (1548716, "instytucje otoczenia biznesu na 10 tys. podmiotów gospodarki narodowej"),
        (473788, "udział nowo zarejestrowanych podmiotów sektora kreatywnego w liczbie nowo zarejestrowanych podmiotów ogółem"),
        (1725013, "podmioty gospodarcze w usługach wyższego rzędu (sekcje J-R) na 1000 ludności"),
        (265616, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja M"),
        (271512, "Osoby fizyczne prowadzące działalność gospodarczą"),
        # (265726, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 ogółem"), # duplicate
        (265365, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja A"),
        (265533, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja B"),
        (266254, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja C"),
        (265830, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja D"),
        (266501, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja E"),
        (265586, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja F"),
        (266213, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja G"),
        (265869, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja H"),
        (265296, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja I"),
        (266487, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja J"),
        (265359, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja K"),
        (266513, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja L"),
        (265425, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja N"),
        (265625, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja O"),
        (266142, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja P"),
        (265304, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja Q"),
        (265990, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja R"),
        (266152, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcje S i T"),
        (265372, "Podmioty wpisane do rejestru REGON wg sekcji PKD 2007 Sekcja U"),
        (74107, "Podmioty według klas wielkości ogółem"),
        (74105, "Podmioty według klas wielkości 0 - 9"),
        (74103, "Podmioty według klas wielkości 10 - 49"),
        (74101, "Podmioty według klas wielkości 50 - 249"),
        (74099, "Podmioty według klas wielkości 250 - 999"),
        (74097, "Podmioty według klas wielkości 1000 i więcej"),
        (289548, "liczba obiektów noclegowych"),
        (289506, "liczba miejsc noclegowych"),
        (266823, "Podmioty nowo zarejestrowane"),
        (268082, "Podmioty wyrejestrowane"),
    ],
    "Rynek pracy": [
        (79214, "Udział bezrobotnych w liczbie osób w wieku produkcyjnym"),
        (1650726, "Pracujący - nowe dane ogółem"),
        (1650728, "Pracujący - nowe dane kobiety"),
        (1650727, "Pracujący - nowe dane mężczyźni"),
        (10514, "Bezrobotni wg płci ogółem"),
        (10515, "Bezrobotni wg płci kobiety"),
        (33484, "Bezrobotni wg płci mężczyźni"),
    ],
    "Infrastruktura": [
        (288061, "Zmieszane odpady komunalne z gospodarstw domowych przypadające na 1 mieszkańca"),
        (288060, "Odpady zebrane selektywnie z gospodarstw domowych w relacji do ogółu odpadów z gosp domowych"),
        (283824, "Zużycie wody z wodociągów na 1 korzystającego [m3]"),
        (79133, "Udział ludności korzystającej z sieci wodociągowa"),
        (79130, "Udział ludności korzystającej z sieci kanalizacyjna"),
        (79127, "Udział ludności korzystającej z sieci gazowa"),
        (79142, "Sieć rozdzielcza na 100 km2 wodociągowa"),
        (79139, "Sieć rozdzielcza na 100 km2 kanalizacyjna"),
        (79136, "Sieć rozdzielcza na 100 km2 gazowa"),
        (194828, "Lesistość"),
        (1646047, "Udział obszarów prawnie chronionych w powierzchni ogółem"),
        (1621852, "udział powierzchni terenów zieleni w powierzchni ogółem"),
        (1612162, "wodociąg długość eksploatowanej sieci wodociągowej (rozdzielczej i przesyłowej) km"),
        (490, "wodociąg przyłącza prowadzące do budynków mieszkalnych i zbiorowego zamieszkania"),
        (494, "kanalizacja długość czynnej sieci ogółem km"),
        (495, "kanalizacja przyłącza prowadzące do budynków mieszkalnych i zbiorowego zamieszkania"),
        (1725887, "Gaz długość czynnej sieci ogółem m"),
        (1725890, "Gaz czynne przyłącza do budynków ogółem (mieszkalnych i niemieszkalnych)"),
        (54841, "odpady zebrane w ciągu roku ogółem"),
        (54842, "odpady zebrane w ciągu roku ogółem z gospodarstw domowych"),
    ],
    "Transport": [
        (1365541, "drogi dla rowerów na 100 km2"),
        (288080, "drogi dla rowerów ogółem"),
    ],
    "Bezpieczeństwo": [
        (1365290, "Zdarzenia wymagające udziału jednostek ochrony przeciwpożarowej na 1000 ludności"),
        (1365274, "Ochrona przeciwpożarowa zdarzenia ogółem"),
        (1365275, "Ochrona przeciwpożarowa pożary razem"),
        (1365280, "Ochrona przeciwpożarowa miejscowe zagrożenia razem"),
        (1365286, "Ochrona przeciwpożarowa alarmy fałszywe razem"),
    ],
    "Finanse": [
        (76037, "Dochody gminy ogółem"),
        (76477, "Wydatki gminy ogółem"),
        (76964, "Wydatki gminy na 1 mieszkańca"),
        (76973, "Dochody gminy na 1 mieszkańca"),
        (77005, "Źródła dochodów subwencja"),
        (149576, "Źródła dochodów dotacje"),
        (76070, "Źródła dochodów dochody własne"),
        (76067, "Źródła dochodów własnych dochody podatkowe - podatek rolny"),
        (101127, "Źródła dochodów własnych dochody podatkowe - podatek leśny"),
        (76077, "Źródła dochodów własnych dochody podatkowe - podatek od nieruchomości"),
        (76074, "Źródła dochodów własnych dochody podatkowe - podatek od środków transportowych"),
        (1601740, "Źródła dochodów własnych dochody podatkowe - podatek od spadków i darowizn"),
        (76040, "Źródła dochodów własnych dochody podatkowe - podatek od czynności cywilnoprawnych"),
        (395080, "Źródła dochodów własnych dochody podatkowe - podatek od działalności gospodarczej osób fizycznych, opłacany w formie karty podatkowej"),
        (76049, "Źródła dochodów własnych udziały w podatkach stanowiących dochody budżetu państwa razem"),
        (76046, "Źródła dochodów własnych udziały w podatkach stanowiących dochody budżetu państwa podatek dochodowy od osób fizycznych"),
        (76043, "Źródła dochodów własnych udziały w podatkach stanowiących dochody budżetu państwa podatek dochodowy od osób prawnych"),
        (76061, "Źródła dochodów własnych wpływy z opłaty skarbowej"),
        (395083, "Źródła dochodów własnych wpływy z opłaty eksploatacyjnej"),
        (76052, "Źródła dochodów własnych wpływy z usług"),
        (395086, "Źródła dochodów własnych wpływy z opłaty targowej"),
        (76064, "Źródła dochodów własnych wpływy z innych lokalnych opłat pobieranych przez jednostki samorządu terytorialnego na podstawie odrębnych ustaw"),
        (76058, "Źródła dochodów własnych dochody z majątku"),
        (148534, "Źródła dochodów własnych pozostałe dochody - środki na dofinansowanie własnych zadań pozyskane z innych źródeł - razem"),
        (202211, "Wydatki wg działów Klasyfikacji Budżetowej Dział 010 - Rolnictwo i łowiectwo"),
        (202205, "Wydatki wg działów Klasyfikacji Budżetowej Dział 020 - Leśnictwo"),
        (202214, "Wydatki wg działów Klasyfikacji Budżetowej Dział 050 - Rybołówstwo i rybactwo"),
        (202217, "Wydatki wg działów Klasyfikacji Budżetowej Dział 100 - Górnictwo i kopalnictwo"),
        (202220, "Wydatki wg działów Klasyfikacji Budżetowej Dział 150 - Przetwórstwo przemysłowe"),
        (202223, "Wydatki wg działów Klasyfikacji Budżetowej Dział 400 - Wytwarzanie i zaopatrywanie w energię elektryczną, gaz i wodę"),
        (202226, "Wydatki wg działów Klasyfikacji Budżetowej Dział 500 - Handel"),
        (202229, "Wydatki wg działów Klasyfikacji Budżetowej Dział 550 - Hotele i restauracje"),
        (202232, "Wydatki wg działów Klasyfikacji Budżetowej Dział 600 - Transport i łączność"),
        (202239, "Wydatki wg działów Klasyfikacji Budżetowej Dział 630 - Turystyka"),
        (202242, "Wydatki wg działów Klasyfikacji Budżetowej Dział 700 - Gospodarka mieszkaniowa"),
        (202245, "Wydatki wg działów Klasyfikacji Budżetowej Dział 710 - Działalność usługowa"),
        (202248, "Wydatki wg działów Klasyfikacji Budżetowej Dział 720 - Informatyka"),
        (202251, "Wydatki wg działów Klasyfikacji Budżetowej Dział 730 - Nauka"),
        (1548645, "Wydatki wg działów Klasyfikacji Budżetowej Dział 730 - Szkolnictwo wyższe i nauka"),
        (202236, "Wydatki wg działów Klasyfikacji Budżetowej Dział 750 - Administracja publiczna"),
        (202253, "Wydatki wg działów Klasyfikacji Budżetowej Dział 751 - Urzędy naczelnych organów władzy państwowej, kontroli i ochrony prawa oraz sądownictwa"),
        (202259, "Wydatki wg działów Klasyfikacji Budżetowej Dział 753 - Obowiązkowe ubezpieczenia społeczne"),
        (202262, "Wydatki wg działów Klasyfikacji Budżetowej Dział 754 - Bezpieczeństwo publiczne i ochrona przeciwpożarowa"),
        (202265, "Wydatki wg działów Klasyfikacji Budżetowej Dział 755 - Wymiar sprawiedliwości"),
        (202268, "Wydatki wg działów Klasyfikacji Budżetowej Dział 756 - Dochody od osób prawnych, od osób fizycznych i od innych jednostek nieposiadających osobowości prawnej oraz wydatki związane z ich poborem"),
        (202271, "Wydatki wg działów Klasyfikacji Budżetowej Dział 757 - Obsługa długu publicznego"),
        (202274, "Wydatki wg działów Klasyfikacji Budżetowej Dział 758 - Różne rozliczenia"),
        (202277, "Wydatki wg działów Klasyfikacji Budżetowej Dział 801 - Oświata i wychowanie"),
        (202280, "Wydatki wg działów Klasyfikacji Budżetowej Dział 803 - Szkolnictwo wyższe"),
        (202283, "Wydatki wg działów Klasyfikacji Budżetowej Dział 851 - Ochrona zdrowia"),
        (202286, "Wydatki wg działów Klasyfikacji Budżetowej Dział 852 - Pomoc społeczna"),
        (202289, "Wydatki wg działów Klasyfikacji Budżetowej Dział 853 - Pozostałe zadania w zakresie polityki społecznej"),
        (202292, "Wydatki wg działów Klasyfikacji Budżetowej Dział 854 - Edukacyjna opieka wychowawcza"),
        (633070, "Wydatki wg działów Klasyfikacji Budżetowej Dział 855 - Rodzina"),
        (202295, "Wydatki wg działów Klasyfikacji Budżetowej Dział 900 - Gospodarka komunalna i ochrona środowiska"),
        (202298, "Wydatki wg działów Klasyfikacji Budżetowej Dział 921 - Kultura i ochrona dziedzictwa narodowego"),
        (273898, "Wydatki wg działów Klasyfikacji Budżetowej Dział 926 - Kultura fizyczna"),
        (76450, "Wydatki majątkowe inwestycyjne"),
    ],
}

class Database:
    def __init__(self, db_type="sqlite", pg_dsn=None):
        self.db_type = db_type
        if db_type == "postgres":
            import psycopg2
            self.conn = psycopg2.connect(pg_dsn)
            self.placeholder = "%s"
        else:
            self.conn = sqlite3.connect(DB_NAME)
            self.placeholder = "?"

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def init_db(self):
        c = self.cursor()
        if self.db_type == "sqlite":
            c.execute('''CREATE TABLE IF NOT EXISTS units (
                            id TEXT PRIMARY KEY,
                            name TEXT,
                            level INTEGER,
                            parentId TEXT
                        )''')
            c.execute('''CREATE TABLE IF NOT EXISTS variables (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            category TEXT,
                            measureUnitName TEXT,
                            lastUpdate TEXT
                        )''')
            c.execute('''CREATE TABLE IF NOT EXISTS data (
                            unit_id TEXT,
                            variable_id INTEGER,
                            year INTEGER,
                            value REAL,
                            attr_id INTEGER,
                            PRIMARY KEY (unit_id, variable_id, year),
                            FOREIGN KEY (unit_id) REFERENCES units(id),
                            FOREIGN KEY (variable_id) REFERENCES variables(id)
                        )''')

            c.execute("CREATE INDEX IF NOT EXISTS idx_units_name ON units(name)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_variables_category ON variables(category)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_data_variable ON data(variable_id)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_data_unit ON data(unit_id)")

            c.execute('''CREATE VIEW IF NOT EXISTS view_full_data AS
                         SELECT
                            d.year,
                            u.id as unit_id,
                            u.name as unit_name,
                            v.id as variable_id,
                            v.name as variable_name,
                            d.value,
                            v.measureUnitName as unit,
                            v.category
                         FROM data d
                         JOIN units u ON d.unit_id = u.id
                         JOIN variables v ON d.variable_id = v.id''')
        else: # postgres
            c.execute('''CREATE TABLE IF NOT EXISTS units (
                            id TEXT PRIMARY KEY,
                            name TEXT,
                            level INTEGER,
                            parentId TEXT
                        )''')
            c.execute('''CREATE TABLE IF NOT EXISTS variables (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            category TEXT,
                            measureUnitName TEXT,
                            lastUpdate TEXT
                        )''')
            c.execute('''CREATE TABLE IF NOT EXISTS data (
                            unit_id TEXT REFERENCES units(id),
                            variable_id INTEGER REFERENCES variables(id),
                            year INTEGER,
                            value REAL,
                            attr_id INTEGER,
                            PRIMARY KEY (unit_id, variable_id, year)
                        )''')

            c.execute("CREATE INDEX IF NOT EXISTS idx_units_name ON units(name)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_variables_category ON variables(category)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_data_variable ON data(variable_id)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_data_unit ON data(unit_id)")

            c.execute('''CREATE OR REPLACE VIEW view_full_data AS
                         SELECT
                            d.year,
                            u.id as unit_id,
                            u.name as unit_name,
                            v.id as variable_id,
                            v.name as variable_name,
                            d.value,
                            v.measureUnitName as unit,
                            v.category
                         FROM data d
                         JOIN units u ON d.unit_id = u.id
                         JOIN variables v ON d.variable_id = v.id''')
        self.commit()

def api_get(endpoint, params=None, retries_in_round=0):
    global current_key_index

    # Rate limiting:
    # Anonymous: 5 req/s
    # Registered: 10 req/s
    # We use a conservative 0.1s or 0.2s delay.
    delay = 0.1 if API_KEYS else 0.2
    time.sleep(delay)

    url = f"{BASE_URL}/{endpoint}"
    headers = {}
    if API_KEYS:
        headers["X-ClientId"] = API_KEYS[current_key_index]

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 429:
            if API_KEYS and retries_in_round < len(API_KEYS):
                old_key = API_KEYS[current_key_index]
                current_key_index = (current_key_index + 1) % len(API_KEYS)
                new_key = API_KEYS[current_key_index]
                print(f"Rate limit exceeded for key {old_key}. Switching to next key.")
                return api_get(endpoint, params, retries_in_round + 1)
            else:
                print("Rate limit exceeded for all keys (or anonymous). Waiting 60 seconds...")
                time.sleep(60)
                return api_get(endpoint, params, 0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def fetch_units(level):
    print(f"Fetching units for level {level}...")
    params = {"level": level, "page-size": 100}
    units = []
    page = 0
    while True:
        params["page"] = page
        data = api_get("units", params)
        if not data or "results" not in data:
            break
        units.extend(data["results"])
        if "next" not in data.get("links", {}):
            break
        page += 1
    return units

def save_units(db, units, level):
    c = db.cursor()
    for u in units:
        if db.db_type == "sqlite":
            c.execute("INSERT OR REPLACE INTO units (id, name, level, parentId) VALUES (?, ?, ?, ?)",
                      (u["id"], u["name"], level, u.get("parentId")))
        else:
            c.execute('''INSERT INTO units (id, name, level, parentId) VALUES (%s, %s, %s, %s)
                         ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, level = EXCLUDED.level, parentId = EXCLUDED.parentId''',
                      (u["id"], u["name"], level, u.get("parentId")))
    db.commit()

def fetch_variable_metadata(var_id):
    return api_get(f"variables/{var_id}")

def save_variable(db, var_id, name, category, measureUnitName, lastUpdate=None):
    c = db.cursor()
    if db.db_type == "sqlite":
        c.execute("INSERT OR REPLACE INTO variables (id, name, category, measureUnitName, lastUpdate) VALUES (?, ?, ?, ?, ?)",
                  (var_id, name, category, measureUnitName, lastUpdate))
    else:
        c.execute('''INSERT INTO variables (id, name, category, measureUnitName, lastUpdate) VALUES (%s, %s, %s, %s, %s)
                     ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, category = EXCLUDED.category,
                     measureUnitName = EXCLUDED.measureUnitName, lastUpdate = EXCLUDED.lastUpdate''',
                  (var_id, name, category, measureUnitName, lastUpdate))
    db.commit()

def fetch_data_by_variable(var_id, level, year_from, year_to):
    print(f"Fetching data for variable {var_id} at level {level} for {year_from}-{year_to}...")
    years = list(range(year_from, year_to + 1))
    params = {
        "unit-level": level,
        "page-size": 100,
        "year": years
    }
    all_results = []
    page = 0
    while True:
        params["page"] = page
        data = api_get(f"data/By-Variable/{var_id}", params)
        if not data or "results" not in data:
            break
        all_results.extend(data["results"])
        if "next" not in data.get("links", {}):
            break
        page += 1
    return all_results

def save_data(db, var_id, results):
    c = db.cursor()
    for res in results:
        unit_id = res["id"]
        for val in res["values"]:
            year = int(val["year"])
            value = val.get("val")
            attr_id = val.get("attrId")
            if db.db_type == "sqlite":
                c.execute("INSERT OR REPLACE INTO data (unit_id, variable_id, year, value, attr_id) VALUES (?, ?, ?, ?, ?)",
                          (unit_id, var_id, year, value, attr_id))
            else:
                c.execute('''INSERT INTO data (unit_id, variable_id, year, value, attr_id) VALUES (%s, %s, %s, %s, %s)
                             ON CONFLICT (unit_id, variable_id, year) DO UPDATE SET value = EXCLUDED.value, attr_id = EXCLUDED.attr_id''',
                          (unit_id, var_id, year, value, attr_id))
    db.commit()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", help="Specific category to fetch")
    parser.add_argument("--units-only", action="store_true", help="Only fetch units")
    parser.add_argument("--year-from", type=int, default=2014, help="Start year")
    parser.add_argument("--year-to", type=int, default=2025, help="End year")
    parser.add_argument("--force", action="store_true", help="Force fetch even if data exists")
    parser.add_argument("--api-keys", nargs="+", help="Up to 3 API keys")
    parser.add_argument("--db-type", choices=["sqlite", "postgres"], default="sqlite", help="Database type")
    parser.add_argument("--pg-dsn", help="PostgreSQL DSN (e.g., 'dbname=bdl user=postgres password=secret host=localhost')")
    args = parser.parse_args()

    if args.api_keys:
        global API_KEYS
        API_KEYS = args.api_keys[:3]

    db = Database(db_type=args.db_type, pg_dsn=args.pg_dsn)
    db.init_db()

    # Levels: 0 (Polska), 2 (Województwa), 3 (Regiony), 5 (Powiaty), 6 (Gminy)
    levels = [0, 2, 3, 5, 6]

    # 1. Fetch units
    if args.units_only or (not args.category and not args.force):
        # Check if units exist
        c = db.cursor()
        c.execute("SELECT COUNT(*) FROM units")
        if c.fetchone()[0] == 0 or args.force:
            for level in levels:
                units = fetch_units(level)
                save_units(db, units, level)
        if args.units_only:
            db.close()
            return

    # 2. Fetch variables and data
    year_from = args.year_from
    year_to = args.year_to

    categories_to_fetch = [args.category] if args.category else VARIABLES_MAP.keys()

    for category in categories_to_fetch:
        if category not in VARIABLES_MAP:
            print(f"Category {category} not found.")
            continue
        vars_list = VARIABLES_MAP[category]
        print(f"Category: {category}")
        for var_id, user_name in vars_list:
            # 1. Fetch current metadata to check for updates
            metadata = fetch_variable_metadata(var_id)
            if not metadata:
                print(f"Could not fetch metadata for variable {var_id}")
                continue

            api_last_update = metadata.get("lastUpdate")

            # Check if we already have this variable and if it's up to date
            c = db.cursor()
            c.execute(f"SELECT lastUpdate FROM variables WHERE id = {db.placeholder}", (var_id,))
            row = c.fetchone()

            if not args.force and row:
                local_last_update = row[0]
                if api_last_update and local_last_update == api_last_update:
                    # Also check if we actually have data (heuristic)
                    c.execute(f"SELECT COUNT(*) FROM data WHERE variable_id = {db.placeholder} AND year BETWEEN {db.placeholder} AND {db.placeholder}",
                              (var_id, year_from, year_to))
                    if c.fetchone()[0] > 1000:
                        print(f"Skipping variable {var_id}, data is up to date ({local_last_update}).")
                        continue

            # Update metadata
            save_variable(db, var_id,
                          metadata.get("n1", "") + " - " + metadata.get("n2", ""),
                          category,
                          metadata.get("measureUnitName", "unknown"),
                          api_last_update)

            # 2. Fetch data for each level
            print(f"Updating data for variable {var_id}...")
            for level in levels:
                results = fetch_data_by_variable(var_id, level, year_from, year_to)
                if results:
                    save_data(db, var_id, results)
                else:
                    print(f"No data for variable {var_id} at level {level}")

    db.close()
    print("Done!")

if __name__ == "__main__":
    main()
