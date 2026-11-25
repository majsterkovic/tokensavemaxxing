# Równomierna Degradacja Jakości Instrukcji (Badania HumanLayer)

Analiza badań laboratoryjnych przeprowadzonych przez HumanLayer (2026) nad zachowaniem modeli frontier (Claude 3.5/3.7 Sonnet, GPT-4o, Gemini 1.5/2.0 Pro) przy rosnącym wolumenie instrukcji systemowych i reguł workspace.

---

## 1. Mit "Lost in the Middle" w Regułach Systemowych

Przez długi czas panowało przekonanie, że modele ignorują głównie instrukcje umieszczone w środku długiego promptu systemowego ("efekt u-kształtnej uwagi"). Wielu inżynierów próbowało obchodzić to, umieszczając kluczowe reguły na samym początku lub na samym końcu pliku `.cursorrules` lub `.mdc`.

Badanie HumanLayer obaliło tę tezę w odniesieniu do precyzyjnych reguł inżynieryjnych:
- **Degradacja jest równomierna (Uniform Instruction Degradation)**.
- Zwiększenie liczby reguł z 5 do 25 nie sprawia, że model "zapomina reguły 10-15". Sprawia, że model staje się **o kilkadziesiąt procent gorszy w stosowaniu KAŻDEJ pojedynczej reguły w pliku**, włączając w to regułę pierwszą i ostatnią.
- Każda dodatkowa linijka instrukcji rozcieńcza wagę uwagi (attention weight budget) przydzielaną pozostałym wytycznym.

---

## 2. Granice Budżetu Tokenowego dla Reguł Always-On

HumanLayer zmierzyło współczynnik zgodności (Compliance Rate) w zależności od całkowitej liczby tokenów w regułach ładowanych na stałe (`alwaysApply: true`):

| Objętość reguł Always-On | Compliance Rate (zgodność z regułami) | Zjawisko uboczne |
|---|---|---|
| **< 1000 tokenów (~15-30 linii)** | **94% - 98%** | Wysoka precyzja, deterministyczne zachowanie |
| **1000 - 2000 tokenów** | **85% - 90%** | Akceptowalna stabilność, sporadyczne pominięcia |
| **2000 - 4000 tokenów** | **65% - 75%** | Wyraźne gubienie konwencji, powrót do wzorców domyślnych |
| **> 5000 tokenów** | **< 50%** | Halucynacje, ignorowanie zakazanych poleceń, chaos |

### Wniosek: Twardy limit 2000 tokenów
Całkowity budżet dla reguł ładowanych w każdej sesji (`alwaysApply: true`) **nie może przekraczać 2000 tokenów**. Optymalna wartość to **poniżej 800 tokenów**.

---

## 3. Pułapka "Inlining Code Examples"

Jednym z najczęstszych błędów jest wklejanie do reguł całych bloków kodu jako "przykładów idealnego stylu" (np. 80-liniowy komponent Reacta z obsługą błędów):
1. **Pali budżet uwagi**: Taki przykład zjada 600-1000 tokenów, nie wnosząc wiedzy abstrakcyjnej.
2. **Starzeje się natychmiast**: Po pierwszej zmianie w bibliotekach lub architekturze projektu wklejony przykład staje się nieaktualny. Agent zaczyna uczyć się kodu legacy i próbuje narzucać go w nowym kodzie.
3. **Lepsza alternatywa — wskaźnik symboliczny**:
   Zamiast wklejać kod:
   ```markdown
   ❌ ZŁE:
   Oto jak pisać endpoint:
   import { z } from 'zod';
   export async function POST(req: Request) { ...80 linii kodu... }

   ✅ DOBRE:
   Wzorce endpointów API: wzoruj się na strukturze w `src/api/auth/route.ts`.
   ```
   Agent odczyta ten plik tylko wtedy, gdy będzie go potrzebować, a wzorzec zawsze będzie zgodny z aktualnym stanem gałęzi gita.

---

## 4. Zasada Reaktywnego Dodawania Reguł

Reguła ma rację bytu tylko wtedy, gdy spełnia 3 warunki:
1. **Agent realnie popełnił błąd w 2 niezależnych sesjach**.
2. **Narzędzia deterministyczne (Linter, TypeScript compiler, Prettier) nie potrafią tego wymusić**. Jeśli błąd może wyłapać ESLint — skonfiguruj ESLinta, nie twórz reguły LLM.
3. **Reguła ma postać negatywną lub jednoznacznego zakazu/nakazu**:
   - Źle: *"Pamiętaj o dbaniu o czystość architektury i odpowiednie komentarze."* (zero informacji decyzyjnej).
   - Dobrze: *"Nigdy nie używaj `any`. W plikach mutacji zawsze zwracaj `Result<T, AppError>`."*
