import dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path

dotenv.load_dotenv()

embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

prompts_rephrase=PromptTemplate.from_template(""" \n
"Rephrase  the question based ONLY on the following chat history and if the question cannot be answered because the information is not provided in the context then just return the question, Note:no unnecessary text,
:

{chat_history}

Question: {question}
Answer:""")
parser=StrOutputParser()

prompts=PromptTemplate.from_template("""Answer the question based ONLY on the following context:

{context}

Question: {question}
Answer:""")

chain= prompts_rephrase | llm |parser
chain_clean=prompts| llm |parser

def generate_response(user_input: str, chat_history: str,user_id:int) -> str:
    rephrased = chain.invoke({'chat_history': chat_history, 'question': user_input})

    chroma_path=Path(__file__).resolve().parent.parent /"chroma_db"/f"{user_id}"
    if not chroma_path.exists():
        return "I don't have any documents to read yet! Please upload a PDF first so I can answer your questions."

    vector_store=Chroma(persist_directory=str(chroma_path),embedding_function=embeddings)
    print(f"Total vectors in DB for user {user_id}: {vector_store._collection.count()}")
    chunks = vector_store.similarity_search(query=user_input, k=6)

    context = "\n\n".join([chunk.page_content for chunk in chunks])
    # print(context)
    result = chain_clean.invoke({'context': context, 'question': rephrased})

    return result