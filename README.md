# Agente Autônomo Offline (Gamma)

Este projeto implementa um agente de Inteligência Artificial autônomo, projetado para rodar localmente e offline no seu PC, utilizando Modelos de Linguagem de Grande Escala (LLMs) como Qwen e Gemma.

O agente utiliza o framework **LangChain** para orquestrar o raciocínio (ReAct) e a chamada de ferramentas (Tools), permitindo que o LLM interaja com o sistema de arquivos e execute comandos.

## Pré-requisitos

Para rodar este agente, você precisará:

1.  **Python 3.10+** instalado.
2.  **Ollama** instalado e rodando. O Ollama é a maneira mais fácil de servir seus LLMs locais (Gemma, Qwen, etc.) através de uma API compatível com o LangChain.
    *   Instruções de instalação do Ollama: [https://ollama.com/](https://ollama.com/)
3.  O modelo LLM desejado (ex: `gemma:2b`, `qwen:7b`) deve estar baixado no Ollama.
    *   Para baixar um modelo, use o comando: `ollama pull gemma:2b`

## Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/ainteligencia11-art/agente-autonomous.git
cd agente-autonomous
```

### 2. Instalar Dependências

Recomendamos o uso de um ambiente virtual (`venv`):

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Executar o Agente

O arquivo principal é o `main.py`. Ele contém exemplos de como o agente usa as ferramentas.

**Certifique-se de que o Ollama está rodando em `http://localhost:11434` antes de executar.**

```bash
python main.py
```

## Estrutura do Código (`main.py`)

O código está dividido em três partes principais:

1.  **Definição das Ferramentas (`read_file`, `execute_command`):** Funções que o LLM pode chamar. A ferramenta `execute_command` está **simulada** para segurança no ambiente de desenvolvimento. Para uso real no seu PC, você deve substituir a parte de simulação pela execução real usando o módulo `subprocess` do Python.
2.  **Configuração do LLM:** O agente é inicializado com o `Ollama(model="gemma:2b")`. **Altere o nome do modelo** para o que você deseja usar (ex: `qwen:7b`).
3.  **Loop do Agente (ReAct):** O `create_react_agent` e o `AgentExecutor` orquestram o processo de raciocínio e ação do LLM.

## Próximos Passos (Para Você)

Para tornar o agente totalmente funcional no seu PC, você deve:

1.  **Implementar a Execução Real de Comandos:** No `main.py`, substitua a simulação da função `execute_command` pela lógica real de execução de comandos do sistema operacional (usando `subprocess.run`).
2.  **Adicionar Mais Ferramentas:** Crie ferramentas para tarefas específicas que você deseja que o agente realize (ex: `search_web`, `send_email`, `create_directory`).
3.  **Configuração de Modelo:** Ajuste o `model` no `Ollama` para o seu LLM preferido (`qwen:7b`, `gemma:7b`, etc.).

---
*Desenvolvido por Manus AI (Gamma) para ainteligencia11-art.*
