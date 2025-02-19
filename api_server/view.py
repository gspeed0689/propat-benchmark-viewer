from .models import benchmark_result, Metadata, benchmark_display, benchmark_display_package
from . import controller
from . import mr_logger
from typing import List, Optional, Annotated
from fastapi import APIRouter, Header

router = APIRouter(prefix="/api")

@router.post("/add-result")
def add_result(result: benchmark_result):
    print("✏️/api/add-result called")
    return controller.add_benchmark_result(result)

@router.get("/get-results")
def get_results(
    benchmark: Annotated[str, Header()],
    storage: Annotated[Optional[str], Header()] = None,
    computer: Annotated[Optional[str], Header()] = None
    ) -> benchmark_display | benchmark_display_package:
    return controller.get_results(benchmark, storage, computer)

@router.get("/get-storage")
def get_storage() -> Metadata:
    return controller.get_storage()

@router.get("/get-computers")
def get_computers() -> Metadata:
    return controller.get_computers()

@router.get("/get-benchmark-names")
def get_benchmark_names() -> Metadata:
    return controller.get_benchmark_names()