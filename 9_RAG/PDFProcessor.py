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
    def __init__(self, pdf_folder: str, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
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
            length_function = len,
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
    
    def generate_embeddings(self, chunks: List[Document]) -> List[List[float]]:
        print(f"Generando embeddings para {len(chunks)} chunks...")
        texts = [chunk.page_content for chunk in chunks]

        embeddings = self.embedding_model.embed_documents(texts)

        print("Embeddings generados.")
        return embeddings
    
    def process_pdf(self, pdf_path: Path) -> Dict:
        print("Procesando...")

        documents = self.load_pdf_with_langchain(pdf_path)

        if not documents:
            print("No se pudo cargar el PDF")
            return None
        
        chunks = self.split_documents(documents)

        if not chunks:
            print("No se generaron chunks")
            return None
        
        embeddings = self.generate_embeddings(chunks)

        chunks_data = []
        for i, (chunk, embedding) in enumerate(zip(chunks,embeddings)):
            chunk_info = {
                "chunk_id": i,
                "content": chunk.page_content,
                "metadata": chunk.metadata,
                "embedding": embedding
            }
            chunks_data.append(chunk_info)

        result = {
            "filename": pdf_path.name,
            "filepath": str(pdf_path),
            "num_pages": len(documents),
            "num_chunks": len(chunks),
            "embeddings_dimension": len(embeddings[0]),
            "chunks": chunks_data
        }

        print("Procesamiento completo !!!")

        return result
    
    def process_all_pdfs(self) -> List[Dict]:
        pdf_files = self.get_pdf_files()

        all_results = []

        for pdf_file in pdf_files:
            result = self.process_pdf(pdf_file)
            if result:
                all_results.append(result)
        
        print(f"PROCESAMIENTO COMPLETO: {len(pdf_files)} PDFs fueron procesados exitosamente !!! ")
        return all_results

    def save_results(self, results: List[Dict], output_file: str = "embeddings_output.json"):
        output_path = Path(output_file)

        print(f"Guardando resultados en {output_path}...")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print("Resultados guardados exitosamente")

        total_chunks = sum(r['num_chunks'] for r in results)
        total_pages = sum(r['num_pages'] for r in results)

        print("ESTADÍSTICAS:")
        print(f"    - Total PDFs: {len(results)}")
        print(f"    - Total de páginas: {total_pages}")
        print(f"    - Total de Chunks: {total_chunks}")
        print(f"    - Dimensión de los embeddings: {results[0]['embeddings_dimension']}")
        print(f"    - Promedio de chunks por PDF: {total_chunks / len(results)}")

def main():
    PDF_FOLDER = "./pdfs"
    OUTPUT_FILE = "embeddings_output.json"

    os.makedirs(PDF_FOLDER, exist_ok=True)

    print("========== SISTEMA DE PROCESAMIENTO DE PDFS ==========")

    try:
        processsor = PDFProcessor(pdf_folder=PDF_FOLDER)
        results = processsor.process_all_pdfs()

        if results:
            processsor.save_results(results, OUTPUT_FILE)
            print("Procesamiento completado con exito")
        else:
            print("No se pudieron procesar los PDFs, asegurate de que están en la carpeta ./pdfs")

    except Exception as e:
        print(f"Error durante el procesamiento: {e}")

main()
