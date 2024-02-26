import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader ,TextLoader
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings
import tempfile
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import AzureSearch
from langchain.tools import Tool
from langchain.agents.initialize import initialize_agent
from langchain.agents import AgentType

import yaml

with open('secrete_key/azureopenaikeys.yaml', 'r') as file:
    azurecred = yaml.safe_load(file)

# from Models.agentchatmemory import chatconversationagent

GPT_35_TURBO= azurecred["azureopenai"]["Azure_openai_deployment_35T_name"]                       #os.getenv("Azure_openai_deployment_35T_name")                       #secret["Azure_openai_deployment_35T_name"]
GPT_4_TURBO= azurecred["azureopenai"]["Azure_openai_deployment_4T_name"]             # os.getenv("Azure_openai_deployment_4T_name")                               #secret["Azure_openai_deployment_4T_name"]
GPT_35_TURBO_16K= azurecred["azureopenai"]["Azure_openai_deployment_35T_16k_name"]         #os.getenv("Azure_openai_deployment_35T_16k_name")                      #secret["Azure_openai_deployment_35T_16k_name"]
GPT_4_TURBO_32k=azurecred["azureopenai"]["Azure_openai_deployment_4T_32k_name"]                #os.getenv("Azure_openai_deployment_4T_32k_name")           #secret["Azure_openai_deployment_4T_32k_name"]

AzureDBusername= azurecred["azureopenai"]["username"]
AzureDBpassword= azurecred["azureopenai"]["password"]
AzureDBserver= azurecred["azureopenai"]["server"]
AzureDBdatabasename= azurecred["azureopenai"]["database"]



class chat_gen():
    def __init__(self, model="Provide your Azureopenai model name"):
        self.chat_history=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.model = model

    def load_doc(self,):

        embeddings = OpenAIEmbeddings(
                                openai_api_key =azurecred["azureopenai"]["openai_api_key"],   #os.getenv("openai_api_key"),  #secret["openai_api_key"],
                                openai_api_base =azurecred["azureopenai"]["openai_api_base"], #os.getenv("openai_api_base"), # secret["openai_api_base"],
                                openai_api_type =azurecred["azureopenai"]["openai_api_type"],  #os.getenv("openai_api_type"), #secret["openai_api_type"],
                                openai_api_version =azurecred["azureopenai"]["openai_api_version"],  #os.getenv("openai_api_version"), # secret["openai_api_version"],
                                deployment=azurecred["azureopenai"]["embedding_deployment"],    #os.getenv("embedding_deployment"),    #secret["embedding_deployment"], 
                                chunk_size=1
                                )
        acs = AzureSearch(azure_search_endpoint=azurecred["azureopenai"]["azure_search_endpoint"],
                        azure_search_key=azurecred["azureopenai"]["azure_search_key"],
                        index_name=azurecred["azureopenai"]["index_name"],
                        embedding_function= embeddings.embed_query
                        )
        retriever = acs.as_retriever(include_metadata=True, metadata_key = 'source')


        return retriever


    def load_model(self,model="Provide your Azureopenai model name"):
        llm = AzureChatOpenAI(
                openai_api_key =azurecred["azureopenai"]["openai_api_key"],   #os.getenv("openai_api_key"),   #secret["openai_api_key"],
                openai_api_base =azurecred["azureopenai"]["openai_api_base"],   #os.getenv("openai_api_base"),   # secret["openai_api_base"],
                openai_api_version =azurecred["azureopenai"]["openai_api_version"],  #os.getenv("openai_api_version"),  #secret["openai_api_version"],
                temperature=0,    
                deployment_name=model)
        
        document_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever= self.load_doc() ) 

        #Define the tools. Here we define only one tool that chats with finance documents.
        tools = [
                    Tool(
                        name="QA",
                        func=document_chain.run,
                        description="useful for answering any queries related to the provided documents. It can convert any language used in the query into English, search for the best answer to the required question, and provide the answer in the original language. It also makes proper use of the memory from the chat conversation.",
                        # description="useful for answering any queries related to provided documents and any languages using in the query convert in english language and search the answer for  best required question and provide its provided language also properly use momery of cht conversation.",
                        # description="useful for answering any queries related to provided documents",
                        return_direct=True,
                    )           
                ]

        #Define Agent executor and pass the memory object we created earlier.
        agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=self.chat_history,handle_parsing_errors=True)


        
        return agent_chain

    def ask_pdf(self, model, query):
        answer = self.load_model(model).run(input=query)
        #print(result)
        return answer


if __name__ == "__main__":
    chat = chat_gen()
    print(chat.ask_pdf("what is lamination?"))
    # print(chat.ask_pdf("when did he die?"))