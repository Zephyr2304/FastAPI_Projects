from typing import Optional
from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from uuid import UUID


app = FastAPI(
    title="Project_3",
    description="This is the todo application with various features of fastapi",
    docs_url="/docs",
    redoc_url="/redoc")
