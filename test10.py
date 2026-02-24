from langchain.output_parsers import StructuredOutputParser,ResponseSchema
from langchain_community.llms import tongyi
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain import ConversationChain

API_KEY = 'sk-ce8aa4d016dd4541a87f59cbd9bff46c'
chat = tongyi.Tongyi(api_key=API_KEY)

memory = ConversationBufferMemory()

onversation = ConversationChain(memory=memory,llm=chat)

# onversation.predict(input="我是一个程序员")

rs = onversation.predict(input="我的职业是什么,请简要回答职业名称即可")

print(rs)

print("----------------------------------------------------------------------------")
chat.invoke("我是一个程序员")

rs = chat.invoke("我的职业是什么")

print(rs)