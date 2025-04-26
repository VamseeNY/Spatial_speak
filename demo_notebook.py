import os
import pandas as pd
from langchain.docstore.document import Document
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms.ollama import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_format_csv(csv_path):
    """Load CSV file and format as a readable table."""
    try:
        df = pd.read_csv(csv_path)
        return df.to_markdown(index=False)
    except Exception as e:
        print(f"Error loading {csv_path}: {str(e)}")
        return "CSV data could not be loaded"

def load_experiment_documents(csv_folder, text_folder):
    """Load and format experiment documents with structured metadata."""
    documents = []
    for filename in os.listdir(csv_folder):
        if filename.endswith('.csv'):
            base_name = filename[:-4]
            csv_path = os.path.join(csv_folder, filename)
            txt_path = os.path.join(text_folder, base_name + '.txt')
            
            if not os.path.exists(txt_path):
                print(f"Warning: No text file for {filename}")
                continue
                
            try:
                df = pd.read_csv(csv_path)
                csv_table = df.to_markdown(index=False)
                
                org_data = df['Characteristics: Organism'].unique() if 'Characteristics: Organism' in df.columns else []
                genotype_data = df['Characteristics: Genotype'].unique() if 'Characteristics: Genotype' in df.columns else []
                
                with open(txt_path, 'r', encoding='utf-8') as f:
                    text_content = f.read().strip()
                
                formatted_content = (
                    f"EXPERIMENT: {base_name}\n\n"
                    f"BIOLOGICAL SYSTEM:\n"
                    f"- Organism(s): {', '.join(org_data)}\n"
                    f"- Genotype(s): {', '.join(genotype_data)}\n\n"
                    f"DESCRIPTION:\n{text_content}\n\n"
                    f"KEY DATA COLUMNS:\n{', '.join(df.columns)}\n\n"
                    f"FULL RESULTS:\n{csv_table}"
                )

                metadata = {
                    "experiment": base_name,
                    "organisms": org_data.tolist(),
                    "genotypes": genotype_data.tolist(),
                    "data_columns": df.columns.tolist()
                }
                
                documents.append(Document(
                    page_content=formatted_content,
                    metadata=metadata
                ))
                
            except Exception as e:
                print(f"Error processing {base_name}: {str(e)}")
    
    return documents

# Configuration
text_folder = r"llama stuff\Intros"
csv_folder = r"llama stuff\Downloaded Samples"
model_name = "llama3.2:3b"

# Load and process documents
documents = load_experiment_documents(csv_folder, text_folder)

# Split documents for better retrieval
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\nEXPERIMENT:", "\n\nDESCRIPTION:", "\n\nDATA RESULTS:"]
)

split_docs = text_splitter.split_documents(documents)

# Initialize embeddings and vector store
embeddings = OllamaEmbeddings(model=model_name)
vectorstore = FAISS.from_documents(split_docs, embeddings)

# New prompt template focusing on biological analysis
qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a plant biology research analyst. Analyze this experimental data to answer agricultural questions:

Context:
{context}

Question: {question}

Follow these steps:
1. Identify relevant experiments mentioning the topic in the user query
2. Examine "Characteristics: Organism" and "Factor Value:" columns
3. Compare different gravity/spaceflight conditions
4. Look for growth patterns or stress responses
5. Connect findings to Earth agriculture potential

Present your answer with:
- 3 key observations from the data
- Specific experimental conditions used
- Quantitative results from tables
- Relevance to crop cultivation

If no data exists on the input topic, state that clearly."""
)

# Modified QA chain with metadata filtering
qa_chain = RetrievalQA.from_chain_type(
    llm=Ollama(model=model_name, temperature=0.2),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "filter": {"organisms": "Oryza sativa"}  # Metadata filter
        }
    ),
    chain_type_kwargs={"prompt": qa_prompt},
    return_source_documents=True
)

def analyze_agricultural_trends(query):
    """Specialized analysis function for agricultural insights."""
    response = qa_chain({"query": query})
    
    result = f"Agricultural Analysis:\n{response['result']}\n\nSupporting Evidence:\n"
    
    for doc in response["source_documents"]:
        if "Oryza sativa" in doc.metadata.get("organisms", []):
            result += f"Experiment {doc.metadata['experiment']}:\n"
            result += f"- Conditions Tested: {doc.metadata.get('data_columns', [])}\n"
            result += f"- Key Parameters: {[c for c in doc.metadata['data_columns'] if 'Factor Value' in c]}\n"
            result += f"- Sample Description: {doc.page_content[:300]}...\n\n"
    
    return result
