from . import database
from . import models
from . import mr_logger
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from typing import List, Optional
from pprint import pprint

def add_benchmark_result(result: models.benchmark_result):
    with Session(database.engine) as session:
        item = insert(database.benchmark_result)
        item = item.values(result.dict())
        session.execute(item)
        session.commit()
    
def get_results(
        benchmark: str, 
        storage: Optional[str] = None,
        computer: Optional[str] = None
    ) -> models.benchmark_display | models.benchmark_display_package:
    mr_logger.logger.debug("🔍")
    with Session(database.engine) as session:
        stmt = select(database.benchmark_result)
        stmt = stmt.where(database.benchmark_result.benchmark_name == benchmark)
        if storage:
            stmt.where(database.benchmark_result.storage_name == storage)
        if computer:
            stmt.where(database.benchmark_result.computer_name == computer)
        results = session.execute(stmt).all()
    # mr_logger.logger.debug(dir(results[0][0]))
    storage_list = list({x[0].storage_name for x in results})
    computer_list = list({x[0].computer_name for x in results})
    # mr_logger.logger.debug(storage_list)
    # mr_logger.logger.debug(computer_list)
    return_results = []
    existing_pairs = {}
    for computer in computer_list:
        for storage in storage_list:
            if computer not in existing_pairs.keys():
                existing_pairs[computer] = []
            benchmark_result_list =[x[0].benchmark_elapsed_time for x in results if x[0].computer_name == computer and x[0].storage_name == storage]
            if len(benchmark_result_list) > 0 and storage not in existing_pairs[computer]:
                current_object = models.benchmark_display(storage_name=storage,
                                                            computer_name=computer,
                                                            benchmark_results=benchmark_result_list)
                return_results.append(current_object)
            existing_pairs[computer].append(storage)
    if len(return_results) > 0:
        return models.benchmark_display_package(benchmarks=return_results)
    # elif return_results == 1:
    #     return return_results[0]

def get_storage():
    with Session(database.engine) as session:
        stmt = select(database.benchmark_result.storage_name)
        stmt = stmt.distinct()
        results = session.execute(stmt).all()
    results = models.Metadata(items=[x[0] for x in results])
    return results

def get_computers():
    with Session(database.engine) as session:
        stmt = select(database.benchmark_result.computer_name)
        stmt = stmt.distinct()
        results = session.execute(stmt).all()
    results = models.Metadata(items=[x[0] for x in results])
    return results

def get_benchmark_names():
    with Session(database.engine) as session:
        stmt = select(database.benchmark_result.benchmark_name)
        stmt = stmt.distinct()
        results = session.execute(stmt).all()
    results = models.Metadata(items=[x[0] for x in results])
    return results