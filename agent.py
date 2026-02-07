import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from langchain_community.tools.pubmed.tool import PubmedQueryRun

# === API KEY DESDE VARIABLES DE ENTORNO ===
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#creacion de herramientas propias

#1-CONVERSION DE MEDIDAS PARA PODER HACER EL CALCULO DE INDICE DE MASA CORPORAL
@tool
def convertir_medidas(pies: float, libras: float) -> dict:
    """
    Convierte pies a centímetros y libras a kilogramos.
    """
    altura_cm = pies * 30.48
    peso_kg = libras * 0.453592
    return {
        "altura_cm": round(altura_cm, 2),
        "peso_kg": round(peso_kg, 2)
    }

#2-CALCULO DEL INDICE DE MASA CORPORAL
@tool
def calcular_imc(peso_kg: float, altura_cm: float) -> dict:
    """
    Calcula el Índice de Masa Corporal (IMC).
    Incluye validaciones para evitar valores físicamente imposibles.
    """

    # Validaciones de tipo
    if peso_kg <= 0 or altura_cm <= 0:
        return {"error": "El peso y la altura deben ser valores positivos."}

    # Rangos humanos razonables
    if peso_kg > 500:
        return {"error": "El peso ingresado es irreal para una persona."}

    if altura_cm < 50 or altura_cm > 300:
        return {"error": "La altura ingresada es irreal para una persona."}

    altura_m = altura_cm / 100
    imc = peso_kg / (altura_m ** 2)

    return {"imc": round(imc, 2)}


#3-CLASIFICACION DE MASA CORPORAL
@tool
def clasificar_imc(imc: float) -> str:
    """
    Clasifica el IMC según rangos de la OMS.
    Incluye validaciones para evitar valores inválidos.
    """

    # Validaciones básicas
    if imc is None:
        return "Error: el IMC no puede ser nulo."

    if not isinstance(imc, (int, float)):
        return "Error: el IMC debe ser un número."

    if imc <= 0:
        return "Error: el IMC debe ser un número positivo."

    if imc > 100:
        return "Error: el IMC ingresado es irreal."

    # Clasificación OMS
    if imc < 18.5:
        return "Bajo peso"
    elif imc <= 24.9:
        return "Adecuado"
    elif imc <= 29.9:
        return "Sobrepeso"
    elif imc <= 34.9:
        return "Obesidad grado 1"
    elif imc <= 39.9:
        return "Obesidad grado 2"
    else:
        return "Obesidad grado 3"

#externa pubmed
pubmed_tool = PubmedQueryRun()

llm = ChatOpenAI(temperature=0)

#todas las tools
tools = [
    convertir_medidas,
    calcular_imc,
    clasificar_imc,
    pubmed_tool
]

memory = MemorySaver()

#prompt
system_prompt = (
 """
Eres un asistente que usa herramientas.
Solo puedes:
- Convertir medidas (pies/libras a cm/kg)
- Calcular el IMC
- Clasificar el IMC según la OMS
- Buscar información médica general en PubMed

No brindes diagnósticos clínicos.
No expliques conceptos médicos por tu cuenta.

Si no sabes la respuesta o no puedes resolver la tarea con las herramientas disponibles,
indica que no puedes ayudar y discúlpate brevemente.

Si una herramienta devuelve un error, informa el error al usuario y no continúes el flujo.

Si la consulta no está relacionada con estos temas, responde que no puedes ayudar.
"""
)
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
    checkpointer=memory
)


def run_agent(user_input, thread_id="streamlit"):
    config = {"configurable": {"thread_id": thread_id}}
    response = ""

    for step in agent.stream(
        {"messages": [HumanMessage(content=user_input)]},
        config,
        stream_mode="values"
    ):
        response = step["messages"][-1].content

    return response
