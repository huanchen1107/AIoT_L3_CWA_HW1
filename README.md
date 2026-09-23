# 🌤️ Taiwan Weather Forecast Dashboard
### AI 創新微課程 — L3 CWA Weather App

> **從氣象資料到互動式天氣預報應用**  
> 用程式探索天氣・用資料看見台灣・用 AI 實現更多可能

---

## 📖 課程簡介

本專案是「AI 創新微課程」的第三單元，帶領學員從零開始，透過 **中央氣象署（CWA）Open Data API**，學習如何取得真實天氣資料、進行資料處理與儲存，並最終建立一個互動式台灣天氣預報 Web App。

---

## 🛠️ 技術棧

| 技術 | 用途 |
|------|------|
| **Python** | 主要程式語言 |
| **CWA Open Data API** | 中央氣象署天氣資料來源 |
| **JSON** | API 回傳資料格式解析 |
| **Pandas** | 資料整理與預覽 |
| **SQLite** | 本地資料庫儲存氣溫資料 |
| **Streamlit** | 快速建立互動式 Web App |
| **Folium** | 台灣地圖視覺化 |
| **GitHub** | 版本管理與專案備份 |

---

## 📚 課程大綱（共 24 節）

### 🔹 Part 1：資料取得與解析
1. **課程介紹** — 課程目標、學習地圖、專案成果展示
2. **台灣的天氣與生活** — 天氣影響生活、資料驅動決策、智慧應用案例
3. **中央氣象署 CWA Open Data 平台** — 註冊帳號、取得 API Key、選擇資料集
4. **API 資料取得** — 使用 `requests` 取得 JSON 資料
5. **JSON 資料結構解析** — 找到氣溫資料的位置（MinT / MaxT）
6. **提取最高與最低氣溫** — 資料分析與處理

### 🔹 Part 2：資料儲存與管理
7. **資料整理與預覽** — 使用 Pandas 觀察資料
8. **建立 SQLite 資料庫** — 儲存氣溫資料至 `data.db`
9. **資料庫設計** — `TemperatureForecasts` 資料表架構
10. **查詢資料驗證** — 使用 SQL 語法檢查資料正確性

### 🔹 Part 3：Web App 開發
11. **Streamlit 入門** — 安裝環境、基本結構、Hello World
12. **從資料庫讀取資料** — 使用 SQL 查詢顯示氣溫
13. **下拉選單選擇地區** — 互動式地區選擇
14. **繪製折線圖** — 一週最高與最低氣溫視覺化
15. **顯示資料表格** — 清楚呈現一週天氣預報資料
16. **整合 Web App 介面** — 選地區看氣溫預報完整介面

### 🔹 Part 4：進階功能與優化
17. **進階：台灣地圖視覺化** — 使用 Folium × Streamlit
18. **選擇日期顯示地圖** — 互動式天氣地圖
19. **完整成果展示** — Taiwan Weather Dashboard
20. **程式碼品質與優化** — 程式結構精簡、錯誤處理、重複執行不重複插入、良好的註解

### 🔹 Part 5：發布與延伸
21. **專案上傳至 GitHub** — 建立 Repository、連結 Git remote、Commit & Push
22. **延伸應用與想法** — 天氣提醒 Line Bot、旅遊行程建議、農業 / 防災應用、結合 AI 做分析
23. **回顧與重點整理** — API、JSON、Pandas、SQLite、Streamlit Web App、AI × Coding 實作流程
24. **下一步：繼續探索** — 更多公開資料 API、AIoT 視覺化應用、打造自己的專業作品集

---

## 🗄️ 資料庫結構

```sql
CREATE TABLE TemperatureForecasts (
    id         INTEGER PRIMARY KEY,
    regionName TEXT,
    dataDate   TEXT,
    min        REAL,
    max        REAL
);
```

---

## 🚀 快速開始

### 1. 安裝相依套件

```bash
pip install requests pandas streamlit folium streamlit-folium
```

### 2. 取得 CWA API Key

前往 [中央氣象署開放資料平台](https://opendata.cwa.gov.tw/) 註冊並申請 API Key。

### 3. 執行資料擷取

```bash
python fetch_weather.py
```

### 4. 啟動 Web App

```bash
streamlit run app.py
```

---

## 📊 專案成果

- ✅ 自動從 CWA API 擷取全台各地區天氣預報
- ✅ 將資料儲存至本地 SQLite 資料庫
- ✅ 互動式地區選擇下拉選單
- ✅ 一週氣溫折線圖視覺化
- ✅ 台灣地圖熱力圖（Folium）
- ✅ 完整 Streamlit Web Dashboard

---

## 📁 專案結構

```
L3 CWA/
├── fetch_weather.py      # 從 CWA API 取得天氣資料
├── app.py                # Streamlit Web App 主程式
├── data.db               # SQLite 資料庫
├── requirements.txt      # Python 相依套件清單
└── README.md             # 本文件
```

---

## 👨‍🏫 講師

**煥哥（Huan）**  
> 「技術可以解決問題，但更重要的是，用技術創造更好的未來！」

- GitHub: [@huanchen1107](https://github.com/huanchen1107)
- Email: huanchen1107@email.com

---

## 📄 授權

本專案為教學用途，歡迎學習參考。  
*AI for Learning, AI for a Better Taiwan* 🇹🇼
