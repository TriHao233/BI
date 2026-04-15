# Kß║┐ Hoß║ích Chi Tiß║┐t: Kiß║┐n Tr├║c Training Offline + Matching Online (TF-IDF + KNN)

## 1. Mß╗Ñc ti├¬u
- T├ích rß╗¥i qu├í tr├¼nh huß║Ñn luyß╗çn v├á phß╗Ñc vß╗Ñ dß╗▒ ─æo├ín ─æß╗â t─âng hiß╗çu n─âng runtime.
- Huß║Ñn luyß╗çn model theo batch/offline tß╗½ `Job_dataset.csv`.
- Khi chß║íy online, chß╗ë load artifacts l├¬n RAM v├á trß║ú kß║┐t quß║ú Top K nhanh theo request.

## 2. Phß║ím vi dß╗» liß╗çu v├á ─æß║ºu v├áo/─æß║ºu ra
### 2.1. Nguß╗ôn dß╗» liß╗çu
- File nguß╗ôn: `Job_dataset.csv`
- Cß╗Öt ch├¡nh sß╗¡ dß╗Ñng:
- `Job_ID`
- `Job_Name`
- `Job_Requirements`
- (T├╣y chß╗ìn) `User_ID`, `User_Skills` cho test nß╗Öi bß╗Ö.

### 2.2. ─Éß║ºu v├áo online
- API nhß║¡n payload gß╗ôm:
- `user_skills` (chuß╗ùi kß╗╣ n─âng, ╞░u ti├¬n d├╣ng trß╗▒c tiß║┐p)
- `top_k` (mß║╖c ─æß╗ïnh 5)

### 2.3. ─Éß║ºu ra online
- Danh s├ích Top K jobs gß║ºn nhß║Ñt theo cosine distance/similarity.
- Mß╗ùi item gß╗ôm:
- `job_id`
- `job_name`
- `match_score` (chuß║⌐n h├│a vß╗ü khoß║úng 0..1 ─æß╗â dß╗à hiß╗âu)

## 3. Kiß║┐n tr├║c tß╗òng thß╗â
### 3.1. Offline (Training Pipeline)
1. ─Éß╗ìc `Job_dataset.csv`.
2. L├ám sß║ích dß╗» liß╗çu:
- Giß╗» c├íc cß╗Öt cß║ºn thiß║┐t.
- Xß╗¡ l├╜ thiß║┐u dß╗» liß╗çu: `Job_Requirements = ""` nß║┐u null.
3. Lß╗ìc `Unique Jobs`:
- Khuyß║┐n nghß╗ï ╞░u ti├¬n `drop_duplicates(subset=["Job_ID"])`.
- Nß║┐u `Job_ID` kh├┤ng ß╗òn ─æß╗ïnh, fallback theo `Job_Name + Job_Requirements`.
4. Train Model 1 (Translator):
- `TfidfVectorizer.fit()` tr├¬n to├án bß╗Ö `Job_Requirements`.
- Sinh ma trß║¡n `job_vectors` bß║▒ng `transform()`.
5. Train Model 2 (Matcher):
- Khß╗ƒi tß║ío `NearestNeighbors(metric="cosine", algorithm="brute")`.
- `knn.fit(job_vectors)`.
6. Export artifacts:
- `tfidf.pkl`
- `knn_model.pkl`
- `jobs_info.pkl` (dataframe/list map index -> metadata job)

### 3.2. Online (Backend Serving)
1. Backend startup:
- Load `tfidf.pkl`, `knn_model.pkl`, `jobs_info.pkl` v├áo RAM.
2. Mß╗ùi API request:
- Nhß║¡n `user_skills`.
- `tfidf.transform([user_skills])` -> `user_vector`.
- `knn_model.kneighbors(user_vector, n_neighbors=top_k)`.
3. Hß║¡u xß╗¡ l├╜:
- Map index jobs tß╗½ `jobs_info.pkl`.
- ─Éß╗òi distance cosine th├ánh score: `score = 1 - distance`.
- Trß║ú JSON kß║┐t quß║ú.

## 4. Thiß║┐t kß║┐ file v├á th╞░ mß╗Ñc ─æß╗ü xuß║Ñt
- `trainning_model/`
- `main.py` (FastAPI online serving)
- `train_model.py` (script training offline)
- `artifacts/`
- `tfidf.pkl`
- `knn_model.pkl`
- `jobs_info.pkl`
- `requirements.txt`
- `PLAN_CHI_TIET.md`

## 5. Thiß║┐t kß║┐ chi tiß║┐t pipeline offline
### 5.1. B╞░ß╗¢c 1: Data ingestion
- ─Éß╗ìc CSV bß║▒ng pandas.
- Validate cß╗Öt bß║»t buß╗Öc: `Job_ID`, `Job_Name`, `Job_Requirements`.
- Nß║┐u thiß║┐u cß╗Öt, fail sß╗¢m vß╗¢i log r├╡ r├áng.

### 5.2. B╞░ß╗¢c 2: Data cleaning & dedup
- Chuß║⌐n h├│a text:
- lower-case
- trim spaces
- thay nhiß╗üu khoß║úng trß║»ng th├ánh 1 khoß║úng trß║»ng
- Lß╗ìc duplicate.
- Thß╗æng k├¬ sß╗æ l╞░ß╗úng:
- sß╗æ d├▓ng ban ─æß║ºu
- sß╗æ d├▓ng sau dedup
- tß╗ë lß╗ç giß║úm tr├╣ng lß║╖p

### 5.3. B╞░ß╗¢c 3: Train TF-IDF
- Cß║Ñu h├¼nh khuyß║┐n nghß╗ï ban ─æß║ºu:
- `ngram_range=(1,2)`
- `min_df=1` (hoß║╖c 2 nß║┐u dß╗» liß╗çu lß╗¢n)
- `max_features=5000` (t├╣y k├¡ch th╞░ß╗¢c dß╗» liß╗çu)
- Fit tr├¬n `Job_Requirements` ─æ├ú clean.

### 5.4. B╞░ß╗¢c 4: Train KNN matcher
- Model: `NearestNeighbors`
- Cß║Ñu h├¼nh:
- `n_neighbors` kh├┤ng cß╗æ ─æß╗ïnh khi train (set khi query)
- `metric="cosine"`
- `algorithm="brute"` ph├╣ hß╗úp sparse matrix
- Fit trß╗▒c tiß║┐p tr├¬n ma trß║¡n TF-IDF jobs.

### 5.5. B╞░ß╗¢c 5: Export artifacts
- D├╣ng `pickle` hoß║╖c `joblib`.
- `jobs_info.pkl` cß║ºn chß╗⌐a tß╗æi thiß╗âu:
- `Job_ID`
- `Job_Name`
- `Job_Requirements` (─æß╗â debug/giß║úi th├¡ch)
- L╞░u th├¬m metadata training:
- timestamp
- sß╗æ jobs
- version pipeline

## 6. Thiß║┐t kß║┐ chi tiß║┐t backend online
### 6.1. Startup sequence
- Load ─æß╗º 3 artifacts.
- Kiß╗âm tra t├¡nh ─æß╗ông bß╗Ö:
- sß╗æ h├áng `jobs_info` phß║úi khß╗¢p sß╗æ vector m├á `knn_model` ─æ├ú fit.
- Nß║┐u mismatch, chß║╖n service startup.

### 6.2. API contract ─æß╗ü xuß║Ñt
- Endpoint: `POST /api/recommend`
- Request:
```json
{
  "user_skills": "python, fastapi, sql, machine learning",
  "top_k": 5
}
```
- Response:
```json
[
  {
    "job_id": 101,
    "job_name": "Backend Python Engineer",
    "match_score": 0.8123
  }
]
```

### 6.3. Logic request
1. Validate `user_skills` kh├┤ng rß╗ùng.
2. Validate `top_k` trong ng╞░ß╗íng hß╗úp lß╗ç (v├¡ dß╗Ñ: 1..20).
3. Vector h├│a user skills bß║▒ng TF-IDF ─æ├ú load.
4. Query KNN ─æß╗â lß║Ñy distances + indices.
5. Convert score = `1 - distance`.
6. Trß║ú kß║┐t quß║ú ─æ├ú sort giß║úm dß║ºn theo `match_score`.

### 6.4. Error handling
- `400`: input kh├┤ng hß╗úp lß╗ç.
- `500`: lß╗ùi transform/model.
- `503`: artifacts ch╞░a load hoß║╖c load lß╗ùi.

## 7. Kß║┐ hoß║ích triß╗ân khai theo giai ─æoß║ín
### Giai ─æoß║ín A: Chuß║⌐n h├│a training offline
- T├ích logic training ra `train_model.py`.
- Sinh 3 file artifacts v├áo `artifacts/`.
- In log thß╗æng k├¬ sau mß╗ùi lß║ºn train.

### Giai ─æoß║ín B: Chuyß╗ân backend sang chß║┐ ─æß╗Ö load artifacts
- Loß║íi bß╗Å viß╗çc fit model trß╗▒c tiß║┐p trong `main.py`.
- Chß╗ë load artifacts khi startup.
- Cß║¡p nhß║¡t endpoint d├╣ng KNN thay cho t├¡nh cosine to├án bß╗Ö trß╗▒c tiß║┐p.

### Giai ─æoß║ín C: Kiß╗âm thß╗¡ v├á x├íc nhß║¡n chß║Ñt l╞░ß╗úng
- Unit test cho:
- data cleaning
- dedup
- artifact loading
- inference flow
- Integration test API vß╗¢i bß╗Ö mß║½u.

## 8. Ti├¬u ch├¡ nghiß╗çm thu (Definition of Done)
- C├│ thß╗â chß║íy training offline ─æß╗Öc lß║¡p v├á sinh ─æß╗º 3 artifacts.
- Backend khß╗ƒi ─æß╗Öng th├ánh c├┤ng khi c├│ artifacts hß╗úp lß╗ç.
- API `POST /api/recommend` trß║ú Top K jobs trong thß╗¥i gian mß╗Ñc ti├¬u.
- ─Éß║úm bß║úo kß║┐t quß║ú nhß║Ñt qu├ín giß╗»a c├íc lß║ºn gß╗ìi c├╣ng input.

## 9. Chß╗ë sß╗æ vß║¡n h├ánh khuyß║┐n nghß╗ï
- Latency API P50/P95.
- Tß╗ë lß╗ç request lß╗ùi.
- Thß╗¥i gian load artifacts khi startup.
- Sß╗æ l╞░ß╗úng jobs trong artifacts theo tß╗½ng version.

## 10. Rß╗ºi ro v├á c├ích giß║úm thiß╗âu
- Dß╗» liß╗çu nhiß╗àu/tr├╣ng lß║╖p nhiß╗üu -> t─âng sai lß╗çch gß╗úi ├╜:
- Bß╗ò sung b╞░ß╗¢c clean mß║ính h╞ín v├á quy tß║»c dedup r├╡ r├áng.
- OOV (tß╗½ ngo├ái tß╗½ ─æiß╗ân TF-IDF):
- Cß║¡p nhß║¡t train ─æß╗ïnh kß╗│ theo dß╗» liß╗çu mß╗¢i.
- Artifact mismatch giß╗»a c├íc phi├¬n bß║ún:
- D├╣ng c├╣ng `version_id` cho bß╗Ö 3 file khi xuß║Ñt v├á khi load.

## 11. Lß╗ïch chß║íy ─æß╗ü xuß║Ñt
- Training offline ─æß╗ïnh kß╗│: mß╗ùi ng├áy/tuß║ºn t├╣y tß║ºn suß║Ñt cß║¡p nhß║¡t data.
- Triß╗ân khai artifacts theo phi├¬n bß║ún (rolling update).
- C├│ thß╗â fallback vß╗ü phi├¬n bß║ún artifacts tr╞░ß╗¢c ─æ├│ nß║┐u ph├ít sinh lß╗ùi.

## 12. Checklist thß╗▒c thi nhanh
1. Tß║ío `train_model.py` v├á t├ích pipeline offline.
2. Tß║ío th╞░ mß╗Ñc `artifacts/`.
3. Huß║Ñn luyß╗çn v├á export `tfidf.pkl`, `knn_model.pkl`, `jobs_info.pkl`.
4. Refactor `main.py` ─æß╗â load artifacts khi startup.
5. Cß║¡p nhß║¡t endpoint recommend d├╣ng `kneighbors`.
6. Viß║┐t test v├á benchmark latency c╞í bß║ún.
7. Chß╗æt release notes + version artifacts.

---
Plan n├áy b├ím s├ít kiß║┐n tr├║c bß║ín m├┤ tß║ú: Train offline ─æß╗â tß║ío bß╗Ö dß╗ïch + bß╗Ö khß╗¢p, backend online chß╗ë load model l├¬n RAM v├á truy vß║Ñn Top K theo thß╗¥i gian thß╗▒c.
