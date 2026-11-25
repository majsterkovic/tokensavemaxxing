# Szablon Briefu Zadania (Spec-First Task Kickoff)

Użyj tego szablonu na początku nowej sesji czatu, aby wymusić zaplanowanie prac przed rozpoczęciem pisania kodu:

```text
ZADANIE: [Krótki, 1-zdaniowy opis celu, np. Dodanie webhooka dla zdarzeń Stripe invoice.paid]

KONTEKST I WEJŚCIE:
- Wejście: [np. Żądanie POST /api/webhooks/stripe z podpisem w nagłówku stripe-signature]
- Wyjście: [np. Aktualizacja statusu subskrypcji w bazie i wysyłka maila z fakturą]

OGRANICZENIA:
- Użyj istniejącego klienta w `src/lib/stripe.ts`.
- Nie dodawaj nowych bibliotek npm.
- Wymagany test jednostkowy weryfikujący podpis i obsługę błędu.

KROK 1:
Przeanalizuj powiązania w `.cursor/REPO-MAP.md` i przedstaw krótki, 3-5 punktowy plan realizacji oraz wskaż pliki, które planujesz zmodyfikować.
KATEGORYCZNY ZAKAZ PISANIA KODU W TEJ TURZE — czekaj na moją akceptację planu.
```
