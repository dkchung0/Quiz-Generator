from typing import List
from pydantic import BaseModel

class HistoryTestCase(BaseModel):
    content: str = "Reformation"  
    keywords: list[str] = ["Martin Luther", "Roman Catholic Church"] 

class HistoryTestCases(BaseModel):
    cases: List[HistoryTestCase] = [
        HistoryTestCase(content="Reformation", keywords=["Martin Luther", "Roman Catholic Church"]),
        HistoryTestCase(content="World War II", keywords=["J. Robert Oppenheimer"]),
        HistoryTestCase(content="Civil War", keywords=["slavery"])
    ]

class MathTestCase(BaseModel):
    pass
