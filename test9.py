from langchain.output_parsers import StructuredOutputParser,ResponseSchema
from langchain_community.llms import tongyi
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

API_KEY = 'sk-ce8aa4d016dd4541a87f59cbd9bff46c'
chat = tongyi.Tongyi(api_key=API_KEY)
#定义输出结构
response_schemas = [
  ResponseSchema(name="answer",description="问题的答案",type="string"),
  ResponseSchema(name="confidence",description="答案的置信度",type="float")
]
#创建输出解析器
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
#创建提示模板，包含格式化指令
template="""你是一名老师，请用{style}风格回答以下问题,并以JSON格式返回答案和置信度:
问题：{question}
{format_instructions}"""

prompt = PromptTemplate(
    template=template,
    partial_variables = {"format_instructions":output_parser.get_format_instructions()}
)
llm_chain =  prompt | chat 
chunks = []
for chunk in llm_chain.stream({'style':'幽默风趣','question':'勾股定理是什么？'}):
    chunks.append(chunk)
    print(chunk,end='',flush=True)
# filled_prompt = prompt.format(input_text=input_text)
# #获取输出
# resp = chat.invoke(filled_prompt)
# parsed_output = output_parser.parse(resp)
# print(input_text)
# print(parsed_output)