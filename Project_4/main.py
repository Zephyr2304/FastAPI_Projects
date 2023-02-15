from typing import Optional
from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from uuid import UUID


app = FastAPI(
    title="Project_4",
    description="This is the Full Stack todo application with authorization,frontend,backend and database",
    docs_url="/docs",
    redoc_url="/redoc")
