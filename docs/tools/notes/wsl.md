---
title: "Notatka Narzędziowa: WSL (Windows Subsystem for Linux)"
description: "Konfiguracja WSL (Windows Subsystem for Linux) pod kątem wydajności I/O, ripgrep, git i lokalnych modeli GPU."
---

> **Rola w ekosystemie**: Fundament środowiska uruchomieniowego — natywny linuksowy system plików, błyskawiczne operacje I/O, ripgrep, narzędzia kompilacji oraz bezpośredni dostęp do akceleracji GPU (CUDA).

---

## 1. Złota Zasada Wydajności WSL (Krytyczna dla Tokensavemaxxing)

> ⚠️ **BEZWZGLĘDNY NAKAZ: TRZYMAJ KOD W `/home/mariusz/...`**
> Dostęp do plików systemu Windows przez ścieżkę `/mnt/c/...` z poziomu WSL korzysta z mostka 9P. Powoduje to **katastrofalny spadek wydajności I/O (nawet 10× - 20× wolniejszy git status, ripgrep i npm install)**.

- **Dobra ścieżka**: `/home/mariusz/projekty/moj-kod` (natywny linuksowy system plików ext4).
- **Zła ścieżka**: `/mnt/c/Users/mariusz/Desktop/moj-kod`.
- **Dostęp z poziomu Windows**: W eksploratorze Windows wpisz `\\wsl$\Ubuntu\home\mariusz`.

---

## 2. Konfiguracja Zasobów (`.wslconfig`)

W systemie Windows (w pliku `C:\Users\<TwojaNazwa>\.wslconfig`) warto ograniczyć zasoby, aby WSL nie zjadał całej pamięci RAM komputera:

```ini
[wsl2]
# Przydział RAM dla WSL (np. 16GB lub 24GB z dostępnych w maszynie)
memory=16GB

# Liczba rdzeni procesora
processors=8

# Ograniczenie pliku wymiany
swap=4GB

# Bezpośrednie przekazywanie localhost między Windows a WSL
localhostForwarding=true
```

Po zmianie pliku wykonaj restart WSL w PowerShellu Windowsa:
```powershell
wsl --shutdown
```

---

## 3. Przekazywanie Akceleracji GPU (NVIDIA CUDA dla Modeli Lokalnych)

WSL2 natywnie obsługuje akcelerację GPU z poziomu Linuksa:
- Wystarczy zainstalować najnowsze sterowniki NVIDIA GeForce na systemie Windows.
- **Wewnątrz WSL NIE instaluj sterowników graficznych NVIDIA dla Linuksa** — WSL korzysta ze sterownika z Windowsa przez `libcuda.so`.
- Sprawdzenie dostępności GPU w terminalu WSL:
  ```bash
  nvidia-smi
  ```
  Powinno zwrócić Twoją kartę z 12 GB VRAM (np. RTX 3060/4070) oraz wersję CUDA.

---

## 4. Dlaczego WSL Jest Kluczem do Sukcesu Agentów?
1. **Natywny ripgrep i find**: Wyszukiwanie symboli w tysiącach plików trwa poniżej 50 ms.
2. **Spójne środowisko CLI**: Wszystkie narzędzia (Claude Code, OpenCode, Herdr, Python, Docker) działają bez emulatorów i problemów ze ścieżkami Windowsa (backslashes `\`).
