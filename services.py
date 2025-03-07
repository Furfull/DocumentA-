import os
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from workflowState import WorkflowState
from config import model

def read_python_file(state: WorkflowState) -> WorkflowState:
    uploaded_file = state["file_path"]
    
    if uploaded_file is None:
        raise ValueError("Nenhum arquivo foi enviado.")
    
    try:
        state["code"] = uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Erro ao ler o arquivo: {str(e)}")
    
    return state

def generate_documentation(state: WorkflowState) -> WorkflowState:
    elements = state["code"]
    estrutura = (state["structure"])
    language = state["language"]

    extra_instruction = ""
    if state.get("crag_analysis"):
        extra_instruction = f"""\nCertifique-se de corrigi os seguintes erros:
        {', '.join(state['crag_analysis'])}."""

    template = ChatPromptTemplate.from_template("""
        Dado o seguinte código:

        {elements}
        Por favor, gere uma documentação técnica para esse código, atendendo fielmente seguintes requisitos:
        1. **Língua:** A documentação deve ser escrita em {language}.
        2. **Estrutura:** A documentação deve apresentar **SOMENTE** os seguinte tópicos: {estrutura}.

        {extra_instruction}
    """)
    chain = template | model
    state["documentation"] = chain.invoke({"elements": elements,
                                        "language": language,
                                        "estrutura": estrutura,
                                        "extra_instruction": extra_instruction})
    return state


def format_documentation(state: WorkflowState) -> WorkflowState:
    print("AQUI NA CRIACAO DO ARQUIVO")
    doc = state["documentation"]
    state["final_doc"] = f"""{doc}"""

    readme_path = os.path.join("README.md")
    with open(readme_path, "w") as readme_file:
        readme_file.write(state["final_doc"])
    print(state["final_doc"])
    return state

def chat_with_memory(state: WorkflowState, user_input: str) -> str:
    code = state['code']
    memory = state["memory"]
    documentation = state['documentation']
    prompt = """
        Você é um assistente de programação. Baseado no seguinte código e documentação, responda à pergunta do usuário.
        Código: {code}
        Documentação: {documentation}
        Memória: {memory}
        Pergunta: {user_input}
    """

    template = ChatPromptTemplate.from_template(prompt)
    chain = template | model 
    response = chain.invoke({"user_input": user_input,
                             "code": code,
                             "documentation": documentation,
                             "memory": memory})

    state["memory"].append(f"Usuário: {user_input}")
    state["memory"].append(f"IA: {response}")
    
    return response

def crag_analysis(state: WorkflowState) -> WorkflowState:
    print("\n", state["cont_errors"])
    if state["cont_errors"] >= 3:
        state["crag_analysis"] = None
        return state

    documentation = state["documentation"]
    estrutura = state["structure"]
    lingua = state["language"]
    
    prompt_template = PromptTemplate(
        input_variables=["documentation", "estrutura", "lingua"],
        template="""A resposta: {documentation}
        1. **DEVE** estar na estrutura desejada: {estrutura}
        2. **DEVE** estar na língua desejada: {lingua}
        Caso não esteja atendendo esses pontos, retorne uma mensagem breve mensagem de qual ponto não está sendo contemplado.
        Caso esteja atendendo todos os pontos **DEVE** retornar **APENAS** "OK".
        """
    )
    
    formatted_prompt = prompt_template.format(
        documentation=documentation,
        estrutura=estrutura,
        lingua=lingua
    )
    
    response = model.invoke(formatted_prompt) 

    print(f"CRAG: \n {response}")
    
    if len(response) >= 5:
        state["crag_analysis"] = response
        state["cont_errors"]+=1
    else:
        state["crag_analysis"] = None
    
    return state