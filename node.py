from langgraph.graph import StateGraph
from services import read_python_file, generate_documentation, format_documentation, crag_analysis
from workflowState import WorkflowState

workflow = StateGraph(WorkflowState)
workflow.add_node("Ler Arquivo", read_python_file)
workflow.add_node("Gerar Documentação", generate_documentation)
workflow.add_node("Crag", crag_analysis)
workflow.add_node("Formatar Documentação", format_documentation)

# Definindo a sequência de execução
workflow.set_entry_point("Ler Arquivo")
workflow.add_edge("Ler Arquivo", "Gerar Documentação")
workflow.add_edge("Gerar Documentação", "Crag")
workflow.add_conditional_edges(
    "Crag",
    lambda state: "Gerar Documentação" if state["crag_analysis"] else "Formatar Documentação"
)
workflow.set_finish_point("Formatar Documentação")

# Construindo e rodando o fluxo
graph = workflow.compile()
print(graph.get_graph().draw_mermaid())