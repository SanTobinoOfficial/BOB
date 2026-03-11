# Polityka Prywatności

**Slap Battles Multi Macro** i **Bot Administracyjny BOB**
Ostatnia aktualizacja: 11 marca 2026 r.

---

## 1. Informacje Ogólne

1.1. Niniejsza Polityka Prywatności opisuje, jakie dane zbierane są przez oprogramowanie **Slap Battles Multi Macro** (dalej: **Makro**) oraz **Bot administracyjny BOB** (dalej: **Bot**), w jakim celu są przetwarzane i jak są chronione.

1.2. Administratorem danych jest właściciel projektu BOB (dalej: **Administrator**).

1.3. Korzystanie z Makra lub Bota oznacza akceptację niniejszej Polityki Prywatności.

---

## 2. Jakie Dane Zbieramy?

### 2.1. Makro (SlapBattlesMultiMacro.exe)

| Dane | Opis | Cel |
|------|------|-----|
| **HWID** (Hardware ID) | Identyfikator sprzętowy komputera, pobierany z `HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid` | Weryfikacja licencji — powiązanie klucza z jednym urządzeniem |
| **Klucz licencyjny** | Ciąg `XXXX-XXXX-XXXX-XXXX` wpisany przez Użytkownika | Autoryzacja dostępu do Makra |
| **Konfiguracja modułów** | Ustawienia każdego modułu (czasy, offsety, adresy webhooków) | Przechowywana wyłącznie lokalnie w `%AppData%\SBMM\` — nie jest wysyłana na zewnątrz |
| **Flaga akceptacji ToS** | Plik `tos_accepted.dat` wskazujący, że Użytkownik zaakceptował Warunki | Przechowywana wyłącznie lokalnie |

**Dane wysyłane na zewnątrz przy pierwszym uruchomieniu:**
- HWID jest wysyłany **jednorazowo** do webhooka Discord Administratora, wyłącznie w celu powiązania klucza z urządzeniem.
- Po powiązaniu HWID z kluczem, przy kolejnych uruchomieniach Makro jedynie odczytuje dane z GitHub Gist w celu weryfikacji klucza — nie wysyła dalszych danych HWID.

### 2.2. Bot Discord

| Dane | Opis | Cel |
|------|------|-----|
| **Klucze licencyjne** | Lista kluczy z ich statusem (aktywny/zbanowany) | Zarządzanie licencjami |
| **HWID** | Identyfikator sprzętowy przypisany do klucza | Weryfikacja licencji |
| **Notatki** | Opcjonalny opis przypisany do klucza przez Administratora (np. imię gracza) | Identyfikacja Użytkownika przez Administratora |
| **Debug code** | Tymczasowy kod debugowania generowany dla klucza | Diagnostyka problemów z licencją |
| **Log aktywności** | Zapis komend wykonanych przez Administratorów (kto, co, kiedy) | Audyt działań administracyjnych |
| **ID Discord** | ID serwera i kanału administratora | Konfiguracja Bota |

**Dane Bota są przechowywane w:**
- Prywatnym GitHub Gist (`licenses.json`) — dostępnym wyłącznie dla Administratora za pomocą osobistego tokenu (GIST_TOKEN).
- Lokalnie na serwerze Replit podczas działania Bota (w pamięci operacyjnej i pliku `licenses.json`).

---

## 3. W Jakim Celu Przetwarzamy Dane?

| Cel | Podstawa prawna |
|-----|-----------------|
| Weryfikacja ważności klucza licencyjnego | Uzasadniony interes Administratora — ochrona przed nieuprawnionym użyciem |
| Powiązanie klucza z urządzeniem (anti-sharing) | Uzasadniony interes Administratora |
| Zarządzanie dostępem (blokowanie/odblokowywanie kluczy) | Uzasadniony interes Administratora |
| Diagnostyka problemów z licencją | Uzasadniony interes Administratora i Użytkownika |

Administrator **nie przetwarza** danych w celach marketingowych, profilowania ani nie sprzedaje danych osobom trzecim.

---

## 4. Komu Udostępniamy Dane?

4.1. Dane zbierane przez Makro i Bota **nie są sprzedawane ani udostępniane stronom trzecim** w celach komercyjnych.

4.2. Dane mogą być dostępne dla:
- **GitHub** — baza kluczy `licenses.json` przechowywana jest w prywatnym GitHub Gist. GitHub przetwarza dane zgodnie z własną [Polityką Prywatności](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
- **Discord** — HWID wysyłany jest do webhooka Discord. Discord przetwarza dane zgodnie z własną [Polityką Prywatności](https://discord.com/privacy).
- **Replit** — Bot hostowany jest na platformie Replit. Replit przetwarza dane zgodnie z własną [Polityką Prywatności](https://replit.com/site/privacy).

4.3. W przypadku nałożenia obowiązku prawnego, Administrator może być zobligowany do udostępnienia danych organom ścigania lub innym uprawnionym organom.

---

## 5. Jak Długo Przechowujemy Dane?

| Dane | Okres przechowywania |
|------|---------------------|
| Klucze licencyjne z HWID | Do momentu ręcznego usunięcia klucza przez Administratora lub zakończenia projektu |
| HWID wysłany przez webhook | Discord przechowuje wiadomości zgodnie ze swoją polityką; Administrator nie przechowuje ich oddzielnie |
| Konfiguracja lokalna Makra | Do momentu ręcznego usunięcia plików z `%AppData%\SBMM\` przez Użytkownika |
| Flaga akceptacji ToS | Do momentu ręcznego usunięcia pliku `tos_accepted.dat` przez Użytkownika |
| Logi administracyjne Bota | Sesyjnie — logi kasowane są po restarcie Bota |

---

## 6. Bezpieczeństwo Danych

6.1. Baza licencji (`licenses.json`) przechowywana jest w **prywatnym** GitHub Gist, dostępnym wyłącznie za pomocą tokenu z ograniczonym zakresem uprawnień (`gist` scope).

6.2. Token dostępowy (`GIST_TOKEN`) oraz token Bota (`DISCORD_TOKEN`) przechowywane są jako zaszyfrowane zmienne środowiskowe w Replit (Secrets) i **nie są nigdy umieszczane w repozytorium kodu**.

6.3. Administrator stosuje zasadę minimalnych uprawnień — dostęp do komend Bota posiadają wyłącznie upoważnione osoby.

6.4. Użytkownik przyjmuje do wiadomości, że żaden system bezpieczeństwa nie jest w 100% odporny na ataki, a Administrator dołoży starań w celu ochrony danych.

---

## 7. Prawa Użytkownika

Użytkownik ma prawo do:

- **Dostępu** — uzyskania informacji, jakie dane dotyczące jego klucza/HWID są przechowywane (poprzez kontakt z Administratorem).
- **Korekty** — skorygowania błędnych danych (np. notatki przypisanej do klucza).
- **Usunięcia** — żądania usunięcia swojego klucza i powiązanego HWID z bazy danych (skutkuje trwałą utratą dostępu do Makra).
- **Resetowania HWID** — przeniesienia licencji na nowe urządzenie poprzez kontakt z Administratorem.

Aby skorzystać z powyższych praw, skontaktuj się z Administratorem przez serwer Discord projektu BOB.

---

## 8. Pliki Lokalne Tworzone przez Makro

Makro tworzy następujące pliki na komputerze Użytkownika (w `%AppData%\SBMM\`):

| Plik | Zawartość |
|------|-----------|
| `portal_config.ini` | Ustawienia modułu BOB (Portal) |
| `trap_config.ini` | Ustawienia modułu Trap |
| `obby_config.ini` | Ustawienia modułu Obby Mastery |
| `replica_config.ini` | Ustawienia modułu Replica Bob |
| `manualbob_config.ini` | Ustawienia modułu Manual Bob |
| `critglove_config.ini` | Ustawienia modułu Critical Glove |
| `tos_accepted.dat` | Flaga potwierdzenia akceptacji Warunków |

Pliki te zawierają **wyłącznie ustawienia lokalne** i nie są wysyłane na zewnątrz.
Użytkownik może je w dowolnym momencie usunąć — przy kolejnym uruchomieniu Makro odtworzy je z wartościami domyślnymi.

---

## 9. Zmiany w Polityce Prywatności

9.1. Administrator zastrzega sobie prawo do zmiany niniejszej Polityki Prywatności w dowolnym momencie.

9.2. O istotnych zmianach Administrator poinformuje na serwerze Discord projektu BOB.

9.3. Dalsze korzystanie z Usługi po opublikowaniu zmian oznacza ich akceptację.

---

## 10. Kontakt

W przypadku pytań dotyczących przetwarzania danych osobowych lub niniejszej Polityki Prywatności prosimy o kontakt przez serwer Discord projektu BOB.

---

*Niniejsza Polityka Prywatności obowiązuje od 11 marca 2026 r.*
