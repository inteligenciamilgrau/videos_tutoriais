import os
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

chunk_size = 10
percentual_overlap = 0.2

def open_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error: {e}"


#arquivo = "Novo LLama 31 Corrigido Claude.txt"
arquivo = "Novo LLama 31 Perguntas e Respostas.txt"

texto = open_file(arquivo)
filename = os.path.basename(arquivo)
metadatas = [{"nome do arquivo": filename}]


text_splitter = CharacterTextSplitter(separator="***", chunk_size=chunk_size,
#text_splitter = RecursiveCharacterTextSplitter(separators=["}\n{"],chunk_size=chunk_size,
                                      chunk_overlap=int(chunk_size * percentual_overlap),
                                      length_function=len,
                                      is_separator_regex=False,
                                      )


all_splits = text_splitter.create_documents([texto], metadatas=metadatas)
for index, text in enumerate(all_splits):
    print("#####", index + 1, "#####")
    print(text.page_content)
    print(text.metadata)


vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

#question = "Quantos parâmetros tem o maior modelo Llama 3.1?"
question = "Qual o maior Lhama?"
docs = vectorstore.similarity_search_with_score(question, k=4)
len(docs)

for index, doc in enumerate(docs):
    print("Resultado", index + 1)
    print(doc)
    print("")