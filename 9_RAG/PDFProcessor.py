import os 
from pathlib import Path
from typing import List, Dict
import json

# PROCESAMIENTO DE DOCUMENTOS
from langchain_community.document_loaders import PyPDFLoader, PDFMinerLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

class PDFProcessor:
    def __init__(self, pdf_folder: str, model_name: str = "sentence-tranformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.pdf_folder = Path(pdf_folder)
        self.model_name = model_name

        print("Cargando modelo de embeddings...")
        self.embedding_model = HuggingFaceEmbeddings(
            model_name = model_name,
            model_kwargs = {'device': 'cpu'}, # Usar la CPU en caso de no tener GPU (CUDA)
            encode_kwargs = {'normalize_embeddings': True}
        )
        print("Modelo cargado exitosamente :)")

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 50,
            lenght_function = len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def get_pdf_files(self):
        if not self.pdf_folder.exists():
            raise FileNotFoundError(f"La carpeta {self.pdf_folder} no existe")
        
        pdf_files = list(self.pdf_folder.glob("*.pdf"))
        print(f"Encontrados {len(pdf_files)} archivos PDF.")

        return pdf_files
    
    def load_pdf_with_langchain(self, pdf_path):
        documents = []

        try:
            print("Cargando con PyPDFLoader...")
            loader = PyPDFLoader(str(pdf_path))
            documents = loader.load()

            total_text = "".join([doc.page_content for doc in documents])

            if len(total_text.strip()) < 100:
                print("Poco texto extraído, intentando con PDFMinerLoader...")
                loader = PDFMinerLoader(str(pdf_path))
                documents = loader.load()
            else:
                print(f"PDF cargado correctamente ({len(documents)} páginas)")

        except Exception as e:
            print(f"Error con PyPDFLoader: {e}")
            try: 
                print("Intentando con PDFMinerLoader...")
                loader = PDFMinerLoader(str(pdf_path))
                documents = loader.load()
                print(f"PDF cargado correctamente con PDFMinerLoader ({len(documents)} páginas)")
            except Exception as e2:
                print(f"Error al cargar PDF: {e2}")
                return[]
        
        return documents
    
    def split_documents(self, documents: List[Document]):
        chunks = self.text_splitter.split_documents(documents)
        print(f"Documentos divididos en {len(chunks)} chunks")
        return chunks