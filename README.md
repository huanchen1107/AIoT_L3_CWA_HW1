# Taiwan Weather GIS Dashboard
## AIoT L3 — CWA HW1

> **CWA Open Data → Database → Taiwan GIS → GitHub → Vercel**

本作業以中央氣象署（CWA）真實 Open Data 為資料來源，從 API 資料取得開始，經過 ETL 與 SQLite 儲存，再建立本機 Taiwan GIS Web，最後推送 GitHub 並由 Vercel 自動部署。

## 五大 Gate — 進度追蹤

| Gate | 主題 | 狀態 | 備註 |
|---|---|---|---|
| 1 | CWA API | ✅ **PASS** | F-D0047-091, 22縣市, 7天, T/MaxT/MinT/Wx/PoP 全驗證 |
| 2 | Database | ✅ **PASS** | 成功載入 SQLite (data.db)，308筆預報資料 |
| 3 | Taiwan GIS Web | ✅ **PASS** | Streamlit + Folium 互動地圖 (app.py) |
| 4 | GitHub | ⬜ 待開始 | Gate 3 PASS 後方可進行 |
| 5 | Vercel | ⬜ 待開始 | Gate 4 PASS 後方可進行 |

## 核心流程

```text
CWA Government Open Data
        ↓
     REST API
        ↓
       JSON
        ↓
 Parse / Clean / Transform
        ↓
      SQLite
        ↓
   Backend API
        ↓
Taiwan GIS Web
Leaflet + OpenStreetMap + GeoJSON
        ↓
      GitHub
        ↓
      Vercel
        ↓
   Public Website
```

## Gate 1 — CWA API ✅ PASS

**驗證日期：** 2026-09-23  
**Dataset：** `F-D0047-091`（全臺縣市7天天氣預報）  
> 注意：workflow 指定 F-D0047-093，該 ID CWA 尚未上線（404）。F-D0047-091 為已發布的等價 dataset，具備相同 Locations schema 與完整欄位。

**實際 JSON Schema：**
```text
records.Locations[0].Location[]
  └── LocationName
  └── WeatherElement[]
        ├── 平均溫度   (T)   — 14 periods × 12hr = 7 days
        ├── 最高溫度   (MaxT)
        ├── 最低溫度   (MinT)
        ├── 天氣現象   (Wx)
        └── 12小時降雨機率 (PoP)
```

**Gate 1 PASS Checklist：**
```text
[PASS] Dataset = F-D0047-091
[PASS] CWA authentication success
[PASS] HTTP 200 OK, success = true
[PASS] Real JSON received
[PASS] Actual JSON schema inspected
[PASS] 7-day forecast confirmed (14 x 12hr periods)
[PASS] T / MaxT / MinT / Wx / PoP all confirmed
[PASS] 22/22 Taiwan counties coverage confirmed
[PASS] No mock/fake data
[PASS] No API Key exposed
```

**Output：** `gate1_output.json` (22 counties, no secrets)

## Gate 2 — Database ✅ PASS

**驗證日期：** 2026-09-23  
**資料庫檔案：** `data.db` (SQLite)  
**資料表：** `weather_forecasts`

已將 Gate 1 的真實 CWA JSON 做 ETL 處理。
設計 Duplicate Strategy 採用 `UNIQUE(location_name, forecast_start)` 與 `INSERT OR REPLACE` 策略。

**Gate 2 驗證結果 (SQL SELECT)：**
- 成功插入/更新 `308` 筆預報紀錄，涵蓋所有 `22` 縣市，符合 7 天 (14個 12 小時區段) 資料量 (22 × 14 = 308)。

**Gate 2 PASS Checklist：**
```text
[PASS] Read JSON output from Gate 1
[PASS] SQLite schema configured
[PASS] Duplicate strategy (UNIQUE/REPLACE) implemented
[PASS] ETL process successful
[PASS] Verified via SQL SELECT
[PASS] No GIS work started
```

## Gate 3 — Local Taiwan GIS Web ✅ PASS

**驗證日期：** 2026-09-23  
**Web App 技術：** Streamlit + Folium (`streamlit-folium`)  
**程式碼檔案：** `app.py`  

依據專案設計順序實作完成：
1. **Taiwan Map:** 載入 Folium 的 OpenStreetMap 底圖，置中對齊全台。
2. **Multiple Locations & Marker:** 使用自建立的 `COORDINATES` 取代 CWA 未提供的經緯度，精確點出所有 22 個縣市。
3. **Weather Popup:** 點擊 Marker 顯示地點、天氣狀況、最高與最低氣溫與降雨機率。
4. **Database Integration:** 嚴格遵循要求，資料100%從 `data.db` 載入，沒有任何 hard-code 的氣候預報資料。
5. **Interactive Dashboard:** 
   - 側邊欄提供地區 (Location) 與預報時間 (Forecast Time) 過濾。
   - 高溫智慧變色 Marker：紅色 (>=32°C)、橘色 (>=28°C)、綠色 (常溫)、藍色 (<20°C)。
   - 提供 7 天預報折線圖與完整表格。

**執行方式：**
```bash
streamlit run app.py
```

**Gate 3 PASS Checklist：**
```text
[PASS] Local Map displaying Taiwan
[PASS] Locations matched and parsed to map
[PASS] Popups showing correct Weather & Temperature
[PASS] Data successfully read from SQLite Gate 2 DB
[PASS] Streamlit Interactive map fully built
```

## Gate 4 — GitHub

Local Application 通過 Gate 3 後再整理並 Push。

Push 前必須確認：

- `.env` 未被 commit
- Repository 中沒有 CWA API Key、password、token 或其他 secret
- README 與設計文件完整
- 專案可重新 clone 並依文件執行

完成條件：`GATE 4 = PASS`

## Gate 5 — Vercel Auto Deployment

GitHub Repository 連接 Vercel，設定必要 Environment Variables，由 GitHub push 觸發 Vercel build/deploy。

```text
Code Change → Commit → Push → GitHub → Vercel → Auto Build → Auto Deploy
```

注意：Local SQLite 適合 Gate 2–3 教學，但不可假設 Vercel local filesystem 是永久性 Production Database。若線上版需要持續寫入資料，Cloud Database 視為進階部署需求。

完成條件：`GATE 5 = PASS`

## Security

真正的 CWA Key 只能存在 Local `.env` 與部署平台的 Environment Variables。

```env
CWA_API_KEY=YOUR_CWA_API_KEY
```

`.gitignore` 至少包含：

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc
```

若 Secret 曾被 commit，必須視為 exposed 並 rotate，不能只刪檔案。

## Development Rule

**DO NOT BUILD EVERYTHING AT ONCE.**

每一 Gate 都必須：

```text
BUILD → RUN → TEST → VERIFY → PASS → NEXT GATE
```

Gate FAIL 就停在該 Gate 修正，不得自行跳到下一 Gate。

## Definition of Done

```text
[✅ PASS] Gate 1 — CWA API          (2026-09-23)
              ↓
[✅ PASS] Gate 2 — Database         (2026-09-23)
              ↓
[✅ PASS] Gate 3 — Local Taiwan GIS (2026-09-23)
              ↓
[⬜ TODO ] Gate 4 — GitHub
              ↓
[⬜ TODO ] Gate 5 — Vercel
              ↓
Taiwan Weather GIS Dashboard COMPLETE
```

## Learning Path

這份 HW1 串起五個重要概念：

**Data Acquisition → Data Engineering → GIS Data Application → Software Engineering → Cloud / CI/CD**

詳細設計與驗收規範見 `design.md`。
