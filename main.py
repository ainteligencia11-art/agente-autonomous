import os
from typing import List, Dict, Any

from langchain_community.llms import Ollama
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import BaseTool, tool
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

# --- 1. Definição das Ferramentas (Tools) ---

# O agente precisará de ferramentas para interagir com o sistema de arquivos.
# Vamos criar uma ferramenta de exemplo e uma ferramenta de execução de comandos (simulada).

class FileToolInput(BaseModel):
    """Esquema de entrada para a ferramenta de leitura de arquivos."""
    file_path: str = Field(description="O caminho absoluto ou relativo para o arquivo a ser lido.")

@tool("read_file", args_schema=FileToolInput)
def read_file(file_path: str) -> str:
    """Lê o conteúdo de um arquivo de texto no sistema de arquivos."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"Conteúdo do arquivo '{file_path}':\n---\n{content}\n---"
    except FileNotFoundError:
        return f"ERRO: Arquivo não encontrado no caminho: {file_path}"
    except Exception as e:
        return f"ERRO ao ler o arquivo: {e}"

class CommandToolInput(BaseModel):
    """Esquema de entrada para a ferramenta de execução de comandos."""
    command: str = Field(description="O comando do sistema operacional a ser executado (ex: 'ls -l', 'mkdir novo_dir').")

@tool("execute_command", args_schema=CommandToolInput)
def execute_command(command: str) -> str:
    """
    Executa um comando no terminal do sistema operacional.
    ATENÇÃO: Esta é uma simulação no ambiente de desenvolvimento.
    No seu PC, você precisará de uma implementação real (usando subprocess).
    """
    print(f"SIMULAÇÃO: Comando '{command}' executado.")
    # No ambiente real, você usaria algo como:
    # import subprocess
    # result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # return f"Saída do Comando:\n{result.stdout}\nErro (se houver):\n{result.stderr}"
    
    if "ls" in command:
        return "SIMULAÇÃO DE SAÍDA: main.py, README.md, requirements.txt"
    elif "mkdir" in command:
        return f"SIMULAÇÃO DE SAÍDA: Diretório criado com sucesso para: {command.split(' ')[1]}"
    else:
        return f"SIMULAÇÃO DE SAÍDA: Comando '{command}' executado com sucesso."

# Lista de ferramentas disponíveis para o agente
tools: List[BaseTool] = [read_file, execute_command]

# --- 2. Configuração do LLM (Ollama) ---

# O Ollama é a forma mais fácil de conectar o LangChain aos seus modelos locais (Gemma, Qwen).
# O agente deve estar rodando no seu PC e o Ollama deve estar ativo.
# Substitua 'gemma:2b' pelo nome do modelo que você deseja usar (ex: 'qwen:7b', 'gemma:7b').
# Certifique-se de que o modelo esteja baixado no Ollama.
try:
    llm = Ollama(model="gemma:2b", base_url="http://localhost:11434")
except Exception as e:
    print(f"AVISO: Não foi possível conectar ao Ollama. Certifique-se de que ele está rodando. Erro: {e}")
    # Usar um LLM de fallback para a estrutura, se necessário, mas o foco é o Ollama.
    # Para o propósito de estruturação, vamos prosseguir.
    llm = None 

# --- 3. Criação do Prompt e do Agente ReAct ---

# O prompt ReAct (Reasoning and Acting) é crucial para que o LLM use as ferramentas.
# Ele instrui o LLM a pensar (Thought) e a agir (Action/Action Input).
template = """
Você é um agente de IA autônomo e offline, projetado para executar tarefas no sistema de arquivos do usuário.
Seu objetivo é cumprir as instruções do usuário usando as ferramentas disponíveis.
Você deve sempre raciocinar sobre o próximo passo antes de agir.

REGRAS:
1. Use a ferramenta 'read_file' para ler o conteúdo de arquivos.
2. Use a ferramenta 'execute_command' para executar comandos do sistema operacional.
3. Se a tarefa for concluída ou não houver mais ferramentas a serem usadas, responda com a resposta final.

{tools}

{input}

{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template)

# Cria o agente ReAct
agent = create_react_agent(llm, tools, prompt)

# Cria o executor do agente
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- 4. Função Principal de Execução ---

def run_agent(task: str):
    """Executa o agente com uma tarefa específica."""
    if llm is None:
        print("\n--- ERRO CRÍTICO ---")
        print("O LLM não foi inicializado. Verifique se o Ollama está rodando e se o modelo 'gemma:2b' está baixado.")
        print("A execução do agente foi abortada.")
        return

    print(f"\n--- EXECUTANDO AGENTE ---")
    print(f"TAREFA: {task}")
    
    try:
        result = agent_executor.invoke({"input": task})
        print("\n--- RESULTADO FINAL ---")
        print(result["output"])
    except Exception as e:
        print(f"\n--- ERRO DURANTE A EXECUÇÃO ---")
        print(f"Ocorreu um erro no loop do agente: {e}")

# --- 5. Exemplos de Uso ---

if __name__ == "__main__":
    # Criar um arquivo de teste para a ferramenta 'read_file'
    with open("test_file.txt", "w") as f:
        f.write("Este é um arquivo de teste.\nLinha 2.\nLinha 3.")
    
    # Exemplo 1: Leitura de arquivo
    run_agent("Leia o conteúdo do arquivo 'test_file.txt' e me diga o que está escrito.")
    
    # Exemplo 2: Execução de comando (simulado)
    run_agent("Crie um novo diretório chamado 'relatorios' e depois liste os arquivos.")
    
    # Exemplo 3: Tarefa que não precisa de ferramenta
    run_agent("Qual é a capital do Brasil?")
    
    # Limpeza
    os.remove("test_file.txt")
