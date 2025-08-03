from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def format_chat_history(messages):
    history = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            history += f"Human: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history += f"AI: {msg.content}\n"
    return history.strip()


class character_bot:
    def __init__(self, character_name, txt_path, prompt_style):
        self.character_name = character_name
        self.txt_path = Path(txt_path)
        print("text")

        self.loader = TextLoader(txt_path, encoding='utf-8')
        self.documents = self.loader.load()
        print("loaded")


        self.text_spliter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 150)
        self.split = self.text_spliter.split_documents(self.documents)

        print("spliteed")
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        self.vector_db = FAISS.from_documents(self.split, self.embeddings)
        self.retriever = self.vector_db.as_retriever()

        print("retrieved")

        self.prompt = ChatPromptTemplate.from_messages(prompt_style)
        print("prompt")
        self.model = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.6
        )

        self.chain = (
            {"context" :(lambda x: x["question"]) |  self.retriever | RunnableLambda(format_docs), "question": lambda x:x["question"]}
            | self.prompt
            | self.model
        )
        
        self.chat_history = []

    def get_response(self, user_input):
        chat_history_text = format_chat_history(self.chat_history)
        response = self.chain.invoke({"question": user_input, "chat_history": chat_history_text})


        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response.content))
        
        return response.content
    









