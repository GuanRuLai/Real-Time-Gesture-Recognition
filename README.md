## 專案介紹

本專案是一個 **即時手勢識別應用**，透過 **MediaPipe Hands** 進行手部追蹤，並根據手指關節角度進行手勢判斷。支援多種手勢識別，並透過 `OpenCV` 在畫面上顯示識別結果。

## 功能特點

- **即時手部偵測**：使用 OpenCV 擷取攝影機畫面，並透過 MediaPipe Hands 進行手部偵測。
- **手勢角度計算**：計算 21 個手部關鍵點的角度，判斷手勢類型。
- **支援多種手勢**：
  - `拇指 (good)`
  - `中指 (no!!!)`
  - `拇指、食指、小指 (ROCK!)`
  - `拳頭 (0)`
  - `小指 (weak)`
  - `五指變換 (1~9)`
  - `中指、無名指、小指 (OK)`
- **即時畫面顯示**：將識別結果即時顯示在畫面上。

## 安裝與使用

### 1. 安裝必要的套件

請確保 Python 環境已安裝以下依賴套件：

```bash
pip install opencv-python mediapipe numpy
```

### 2. 執行程式

直接運行 Python 腳本即可啟動手勢識別應用：

```bash
python hand_gesture_recognition.py
```

按 `q` 鍵可退出程式。

## 技術細節

### 1. **即時影像擷取**

- 使用 `cv2.VideoCapture(0)` 開啟攝影機。
- 透過 `cv2.resize()` 進行影像縮放。

### 2. **手勢追蹤與角度計算**

- 透過 `MediaPipe Hands` 取得 21 個手部關鍵點座標。
- 計算各關節角度 (`vector_2d_angle()`)，並基於角度進行手勢判斷。

### 3. **手勢識別邏輯**

- 依據手指彎曲程度（夾角大小）來區分不同手勢。
- 例如，拇指伸直 + 其餘手指彎曲 = 👍 `讚 (good)`。
- 若所有手指皆展開，則判定為 `5`。

## 授權條款

本專案採用 **MIT License**，允許自由使用與修改，惟請保留原始授權條款。
