---
tag: "2026.09.23-current"
status: "CURRENT"
project: "AIoT L3 CWA HW1"
description: "Current five-gate Taiwan Weather GIS development workflow"
source: ".agent/workflows/project_workflow.md"
---

# CURRENT TAG — 2026.09.23

> **Status: CURRENT / ACTIVE**
>
> This is the current project workflow baseline. Antigravity and future development should follow this version unless a newer tagged workflow explicitly supersedes it.

# Taiwan Weather GIS — Project Workflow

## Governing Rule

嚴格依序執行：

```text
Gate 1 CWA API
 → Gate 2 Database
 → Gate 3 Local Taiwan GIS
 → Gate 4 GitHub
 → Gate 5 Vercel
```

**DO NOT BUILD EVERYTHING AT ONCE.**

每個 Gate 必須 `BUILD → RUN → TEST → VERIFY → PASS`。FAIL 時停留在該 Gate 修正。不得使用 mock/fake weather data。

## Gate 1 — CWA API

### Locked Dataset

**Dataset ID: `F-D0047-093`**

CWA 官方文件將 D0047-093 列為「全臺灣各鄉鎮市區預報資料」，可取得未來一週預報。此專案 Gate 1 以此 Dataset 為正式資料來源。

Target requirement:

```text
F-D0047-093
   ↓
All Taiwan township/district forecast data
   ↓
Next 7 days
   ↓
Temperature / MaxT / MinT / Wx / PoP
```

主要 Forecast factors：

- `T` — 溫度
- `MaxT` — 最高溫度
- `MinT` — 最低溫度
- `Wx` — 天氣現象
- `PoP` — 降雨機率（12 小時分段）
- 其他欄位可保留供後續擴充，但 Gate 1 先聚焦上述欄位。

### Authentication / Secret Rule

CWA Authorization Key **不得寫入本文件、source code、README 或 GitHub**。

本機只使用：

```env
CWA_API_KEY=<YOUR_CWA_API_KEY>
```

由 `.env` 提供，並確認 `.env` 已列入 `.gitignore`。

> 如果 Key 曾經出現在聊天、公開文件或其他非秘密位置，應視為 exposed，先到 CWA 重新產生/rotate，再把新的 Key 放入本機 `.env`。不得把實際 Key commit 到 repository。

### Gate 1 Execution

Goal: 從 CWA Open Data API 的 `F-D0047-093` 取得真實一週 Forecast JSON。

1. 使用 Dataset `F-D0047-093`，確認目前官方 API endpoint。
2. 從 `.env` 讀取 `CWA_API_KEY`，log/output 不得顯示完整 Key。
3. 發送真實 CWA HTTP request。
4. 驗證 HTTP status = success。
5. 保存/檢查實際 JSON response structure，再依真實 schema 實作 parser；禁止猜 schema。
6. 先選一個最小案例驗證，例如臺中市中的一個鄉鎮/行政區。
7. 驗證未來一週資料以及 `T`、`MaxT`、`MinT`、`Wx`、`PoP`。
8. 再確認 Dataset 能取得全臺灣各縣市所屬鄉鎮/行政區資料。
9. 建立可供 Gate 2 ETL 使用的乾淨輸出，但 Gate 1 **不得寫入 Database**。
10. 實際 RUN、TEST、VERIFY，留下不含 Secret 的驗證證據。

### Gate 1 PASS Criteria

只有以下全部成立才可回報 `GATE 1 = PASS`：

```text
[ ] Dataset = F-D0047-093
[ ] CWA authentication success
[ ] HTTP request success
[ ] Real JSON received
[ ] Actual JSON schema inspected
[ ] 7-day forecast confirmed
[ ] T confirmed
[ ] MaxT confirmed
[ ] MinT confirmed
[ ] Wx confirmed
[ ] PoP confirmed
[ ] Taiwan township/district coverage confirmed
[ ] No mock/fake weather data
[ ] No API Key exposed in code/log/GitHub
```

禁止實作 SQLite、GIS、GitHub deployment 或 Vercel。Gate 1 FAIL 時留在 Gate 1 修正，不得進入 Gate 2。

## Gate 2 — Database

前提：Gate 1 PASS。

將真實 CWA response 做 ETL 並存入 SQLite。建立 schema、資料驗證與 duplicate strategy，以 SQL SELECT 驗證指定地區及多地區資料。

禁止開始 GIS。

完成才回報：`GATE 2 = PASS`。

## Gate 3 — Local Taiwan GIS

前提：Gate 2 PASS。

依序完成：

```text
3A Taiwan Map
3B One Marker
3C Weather Popup
3D Taiwan Locations
3E Database → GIS
3F Taiwan GeoJSON
3G Interactive Dashboard
```

GIS 優先使用 Leaflet + OpenStreetMap + Taiwan GeoJSON。Weather 必須來自 Database。

完成才回報：`GATE 3 = PASS`。

## Gate 4 — GitHub

前提：Gate 3 PASS。

整理 repository、README/design、requirements 與安全設定。Push 前確認 `.env` 與任何 secret 不在 Git history/current files。

完成才回報：`GATE 4 = PASS`。

## Gate 5 — Vercel

前提：Gate 4 PASS。

連接 GitHub → Vercel，設定 Environment Variables，完成 build/deploy，驗證 public URL，並測試後續 GitHub push 能觸發 auto deployment。

Local SQLite 不視為 Vercel 的永久 Production Database；若需要線上持續寫入，另採 Cloud Database。

完成才回報：`GATE 5 = PASS`。

## Final

只有五 Gate 全 PASS 才回報：

```text
DIC-2 / AIoT L3 CWA HW1 = COMPLETE    (2026-09-23)
```

## Current Baseline

```text
TAG: 2026.09.23-current
STATUS: CURRENT
MAINLINE:
CWA API → Database → Local Taiwan GIS → GitHub → Vercel
```