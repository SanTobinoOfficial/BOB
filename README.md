# BOB v1.3 — Instrukcja użytkownika

## Czym jest BOB?

BOB to narzędzie do **testowania systemów anti-cheat** w grze.
Składa się z 6 niezależnych modułów symulujących automatyczne akcje gracza —
używane wyłącznie do weryfikacji skuteczności zabezpieczeń.

---

## Wymagania

- Windows 10 / 11
- AutoHotkey v2.0 (pobierz z https://www.autohotkey.com)
- Gra uruchomiona w trybie pełnoekranowym lub w oknie

---

## Pierwsze uruchomienie

1. Uruchom plik `BOB.ahk`
2. Przy pierwszym uruchomieniu pojawi się okno z prośbą o klucz licencyjny
3. Wpisz swój klucz (format: `XXXX-XXXX-XXXX-XXXX`)
4. Makro wysyła Twój HWID do administratora — poczekaj na aktywację
5. Po aktywacji uruchom makro ponownie
6. Wybierz moduł z menu głównego

---

## Skróty klawiszowe (globalne)

| Klawisz | Akcja |
|---------|-------|
| F6 | Start / Stop makra (przełącznik) |
| F8 | Bezpieczne wyjście (zapisuje dane) |
| F9 | Panic Stop — natychmiastowe zatrzymanie i zwolnienie klawiszy |

---

## Moduły

### 1. 🌀 BOB — Portal
Automatycznie klika portal, wykrywa kolory baz (niebieska/czerwona),
wykonuje sekwencję ruchu i resetu postaci.

**Jak używać:**
- Ustaw postać przy portalu w grze
- Skonfiguruj współrzędne portalu w Ustawieniach Zaawansowanych
- Naciśnij Start lub F6

**Statystyki:** Pętle sesji, Boby znalezione, Szacowane Boby, Czas sesji, Pętle/h

---

### 2. 🧱 Trap / Brick Master
Automatycznie klika cegłę co ustalony interwał (domyślnie co 5 sekund).
Zlicza cegły aż do osiągnięcia celu (domyślnie 1000).

**Jak używać:**
- Wejdź na testową mapę Trap w grze
- Ustaw cel w Ustawieniach
- Naciśnij Start lub F6

**Statystyki:** Cegły sesji, Cegły łącznie, Postęp %, Czas, Cegły/h, ETA

---

### 3. 🏗️ Obby Mastery — Place Parts
Automatycznie kładzie części Obby co ustalony interwał (domyślnie co 3 sekundy).
Cel: 2000 części (Quest 3 Mastery).

**Jak używać:**
- Wejdź na testową mapę Obby w grze
- Naciśnij Start lub F6

**Statystyki:** Części sesji, Części łącznie, Postęp %, Czas, Części/h, ETA

---

### 4. ⚡ Replica Bob — prosty klik
Automatycznie klika E co 14 sekund (cooldown repliki Boba).
Szansa na uzyskanie Boba: 1/7500.

**Jak używać:**
- Wyekwipuj Replikę Boba w grze
- Naciśnij Start lub F6 — makro klika od razu

**Statystyki:** Kliki sesji, Boby, Szacowane Boby, Czas, Kliki/h

---

### 5. 🖐 Manual Bob — ręczny respawn
Wykonuje sekwencję resetu postaci po naciśnięciu przypisanego klawisza.

**Sekwencja:**
1. (Opcjonalnie) Sleep przed Esc
2. Naciśnięcie Escape
3. Sleep po Esc
4. Naciśnięcie R (Respawn)
5. Sleep po R
6. Naciśnięcie Enter
7. Sleep po Enter

**Domyślny klawisz:** `E`
Klawisz można zmienić w Ustawieniach Zaawansowanych — naciśnij przycisk
"Kliknij i naciśnij klawisz" i wciśnij fizyczny klawisz lub przycisk myszy.

**Statystyki:** Kliki sesji, Boby, Szacowane Boby, Czas, Kliki/h

---

### 6. 💥 Critical Glove — auto klik
Po naciśnięciu przypisanego klawisza wykonuje combo:
Spacja (skok) → Sleep → LPM (kliknięcie w powietrzu = trafienie krytyczne).

**Domyślny klawisz:** Prawy przycisk myszy (`RButton`)
Klawisz można zmienić w Ustawieniach Zaawansowanych.

**Statystyki:** Kliki sesji, Kliki łącznie, Czas, Kliki/h

---

## Ustawienia

Każdy moduł ma własne okno ustawień. Otwierasz je przyciskiem **⚙ Ustawienia**
w oknie modułu.

### Sekcje ustawień

**OPCJE**
- Auto-pauza gdy gra nieaktywna — zatrzymuje makro jeśli gra nie jest aktywna w tle
- Dźwięk przy znalezieniu Boba — sygnał dźwiękowy (3 piknięcia)

**ZAAWANSOWANE**
- Timingowe parametry (Sleep w ms) — sterują szybkością sekwencji
- Klawisz wyzwalacza (Manual Bob, Critical Glove) — fizyczne przypisanie klawisza

**WEBHOOK STATYSTYK**
- URL webhooka Discord — adres do którego wysyłane są statystyki
- Cooldown webhooka (ms) — minimalna przerwa między wysyłkami
- Co ile kliknięć wysyłać statystyki

**DEBUGOWANIE** (chronione kodem PIN)
- Krytyczne ustawienia — zmiana może uszkodzić działanie makra
- Dostępne po wpisaniu kodu PIN (widoczny w panelu administratora)

---

## Webhook Discord

Jeśli podasz URL webhooka Discord w ustawieniach, makro będzie automatycznie
wysyłać statystyki na wybrany kanał. Wiadomości zawierają:
- Liczbę kliknięć / pętli
- Znalezione i szacowane Boby
- Czas sesji i tempo

---

## Historia i dane łączne

Przycisk **📋 Historia** otwiera log sesji. Każda zakończona sesja (Stop lub F8)
jest zapisywana do pliku tekstowego w `%AppData%\BOB\`.

Dane łączne (np. łączna liczba kliknięć od początku) są zachowywane między sesjami.

---

## Pliki konfiguracyjne

Wszystkie ustawienia zapisywane są automatycznie do plików INI w:
`%AppData%\BOB\`

| Plik | Moduł |
|------|-------|
| `portal_config.ini` | BOB (Portal) |
| `trap_config.ini` | Trap / Brick Master |
| `obby_config.ini` | Obby Mastery |
| `replica_config.ini` | Replica Bob |
| `manualbob_config.ini` | Manual Bob |
| `critglove_config.ini` | Critical Glove |
| `license.dat` | Klucz licencyjny |
| `debug_code.dat` | Kod PIN do debugowania |
| `sent_info.dat` | Flaga — info aktywacji wysłane |

---

## Rozwiązywanie problemów

**Makro się nie uruchamia**
- Sprawdź czy AutoHotkey v2.0 jest zainstalowany
- Uruchom plik `.ahk` prawym przyciskiem → "Run as administrator"

**Makro się zatrzymuje samo**
- Włączona opcja "Auto-pauza" — gra musi być aktywna w tle
- Wyłącz Auto-pauzę w Ustawieniach jeśli grasz na innym oknie

**Nieprawidłowy klucz / HWID niezaakceptowany**
- Skontaktuj się z administratorem
- Nie zmieniaj sprzętu komputerowego po aktywacji

**Okno wyboru klawisza zawiesza makro**
- Naciśnij Esc aby anulować
- Okno automatycznie zamknie się po 10 sekundach
