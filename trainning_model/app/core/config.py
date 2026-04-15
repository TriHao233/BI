from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
TFIDF_PATH = ARTIFACTS_DIR / "tfidf.pkl"
KNN_PATH = ARTIFACTS_DIR / "knn_model.pkl"
JOBS_INFO_PATH = ARTIFACTS_DIR / "jobs_info.pkl"

TEMPLATES_DIR = PROJECT_ROOT / "templates"
STATIC_DIR = PROJECT_ROOT / "static"

DATABASE_URL = os.getenv(
    "APP_DATABASE_URL",
    "mysql+pymysql://root:root@127.0.0.1:3306/jobmatch?charset=utf8mb4",
)
SESSION_SECRET = os.getenv("APP_SESSION_SECRET", "change-this-secret-in-production")
PBKDF2_ITERATIONS = int(os.getenv("APP_PBKDF2_ITERATIONS", "120000"))

DEFAULT_ROLE = "candidate"
VALID_ROLES = {"candidate", "recruiter"}
