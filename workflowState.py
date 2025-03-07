from typing import TypedDict, List

class WorkflowState(TypedDict):
    file_path: str
    code: str
    structure: str
    language: str
    documentation: str
    final_doc: str
    memory: List[str] 
    crag_analysis: str
    cont_errors: int