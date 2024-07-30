import os
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter

chunk_size = 100
percentual_overlap = 0.0

def open_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error: {e}"


arquivo = "Novo LLama 31 Corrigido Claude.txt"
#arquivo = "Novo LLama 31 Perguntas e Respostas.txt"

texto = open_file(arquivo)
filename = os.path.basename(arquivo)
metadatas = [{"nome do arquivo": filename}]


text_splitter = CharacterTextSplitter(separator=".", chunk_size=chunk_size,
#text_splitter = RecursiveCharacterTextSplitter(separators=["}\n{"],chunk_size=chunk_size,
                                      chunk_overlap=int(chunk_size * percentual_overlap),
                                      length_function=len,
                                      is_separator_regex=False,
                                      )


texts = text_splitter.create_documents([texto], metadatas=metadatas)
for index, text in enumerate(texts):
    print("#####", index + 1, "#####")
    print(text.page_content)
    print(text.metadata)
