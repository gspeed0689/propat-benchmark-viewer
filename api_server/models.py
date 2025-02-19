from pydantic import BaseModel
from typing import Optional, List

class benchmark_result(BaseModel):
    pk_benchmark_result: Optional[int] = None
    benchmark_version: int
    computer_name: str
    storage_name: str
    benchmark_name: str
    benchmark_elapsed_time: float

class Metadata(BaseModel):
    items: List[str]

class benchmark_display(BaseModel):
    storage_name: str
    computer_name: str
    benchmark_results: List[float]

class benchmark_display_package(BaseModel):
    benchmarks: List[benchmark_display]