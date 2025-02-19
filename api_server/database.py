from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Integer, Double, Date, DateTime, Text, String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import func
from datetime import date, datetime

geobenchbase = declarative_base()

db_string = "sqlite:///benchmarks.sqlite"

engine = create_engine(db_string)

class benchmark_result(geobenchbase):
    __tablename__ = "benchmark_result"
    pk_benchmark_result: Mapped[int] = mapped_column(Integer, primary_key=True)
    benchmark_version: Mapped[int] = mapped_column(Integer, default=17)
    computer_name: Mapped[str] = mapped_column(Text)
    storage_name: Mapped[str] = mapped_column(Text)
    benchmark_name: Mapped[str] = mapped_column(Text)
    benchmark_elapsed_time: Mapped[float] = mapped_column(Double)

geobenchbase.metadata.create_all(engine)