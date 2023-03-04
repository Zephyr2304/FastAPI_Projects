from typing import Optional
from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from uuid import UUID
from database import engine
import models

app = FastAPI(
    title="Project_3",
    description="This is the todo application with various features of fastapi",
    docs_url="/docs",
    redoc_url="/redoc")


models.Base.metadata.create_all(bind=engine)