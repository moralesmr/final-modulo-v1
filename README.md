# Chatbot IMC – Agente Inteligente con Herramientas

Proyecto Integrador – Módulo II
Desarrollo de un agente inteligente con herramientas personalizadas utilizando **LangChain** y **LangGraph**, con interfaz web en **Streamlit**.

## Descripción General

Este proyecto implementa un **agente inteligente especializado en el cálculo del Índice de Masa Corporal (IMC)** y en la **búsqueda de artículos científicos relacionados**, utilizando herramientas propias y una herramienta externa (PubMed).
El agente está diseñado con **restricciones explícitas** para evitar diagnósticos médicos o recomendaciones clínicas, funcionando únicamente como **asistente educativo**.

## Arquitectura del Sistema

**Componentes principales:**

* **Frontend:** Streamlit (interfaz conversacional tipo chat)
* **Agente:** LangChain
* **Memoria y contexto:** LangGraph (`MemorySaver`)
* **Modelo LLM:** ChatOpenAI
* **Herramientas:**

  * Herramientas personalizadas (IMC)
  * Herramienta externa (PubMed)

**Flujo general:**

Usuario → Streamlit → Agente → Tool correspondiente → Respuesta

Cada conversación se gestiona mediante un `thread_id`, permitiendo mantener el contexto dentro de una sesión.

## Herramientas Implementadas

### 1️⃣ `convertir_medidas`

Convierte altura en pies y peso en libras a centímetros y kilogramos.

### 2️⃣ `calcular_imc`

Calcula el Índice de Masa Corporal a partir del peso y la altura.

### 3️⃣ `clasificar_imc`

Clasifica el IMC según los rangos oficiales de la OMS.

### 4️⃣ Herramienta Externa – PubMed

Se utiliza `PubmedQueryRun` para realizar búsquedas de artículos científicos validados.
Se eligió PubMed por tratarse de una base de datos científica validada, especialmente adecuada para consultas relacionadas con salud.

---

## Lógica del Agente

El agente:

* Decide automáticamente qué herramienta utilizar según la consulta
* No responde fuera de los temas permitidos
* No brinda diagnósticos ni recomendaciones médicas
* Detiene el flujo si una herramienta devuelve error

Estas reglas están definidas en el `system_prompt`.

---

## Manejo de Memoria y Contexto

* Se utiliza `MemorySaver` de LangGraph
* Cada `thread_id` representa una conversación independiente
* En Streamlit se usa un único `thread_id` por sesión
* El agente responde siempre considerando el **contexto más reciente**

---

## Ejecución Local

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/chatbot-imc.git
cd chatbot-imc
```

---

### 2️⃣ Crear entorno virtual e instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Configurar variables de entorno (ejecución local)

Para ejecutar la aplicación localmente es necesario configurar la variable de entorno con la API Key de OpenAI.

En sistemas Unix / MacOS:

```bash
export OPENAI_API_KEY=tu_api_key
```

En Windows:

```bat
set OPENAI_API_KEY=tu_api_key
```

---

### 4️⃣ Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en el navegador y permitirá interactuar con el agente de forma conversacional.

NOTA: Además se agrega el archivo ipynb inicial y el archivo pdf con la documentación , arquitectura y reflexiones finales del proyecto.
---

## Despliegue en Streamlit Cloud

La aplicación fue desplegada en **Streamlit Cloud**, permitiendo su uso sin necesidad de ejecución local.

Para el despliegue se utilizó el sistema de **Secrets de Streamlit**, donde se configuró la variable sensible:

```toml
OPENAI_API_KEY = "********"
```

## Consideraciones Éticas y de Seguridad

* El agente **no reemplaza la consulta médica**
* Toda la información es educativa
* Las clasificaciones del IMC se basan en estándares de la OMS
* Se recomienda siempre consultar a un profesional de la salud

## Conclusión

El proyecto demuestra el diseño de un agente inteligente modular, con uso controlado de herramientas, manejo de contexto y despliegue web, aplicando buenas prácticas de seguridad y responsabilidad en el uso de IA Generativa.
