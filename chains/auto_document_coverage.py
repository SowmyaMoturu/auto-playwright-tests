from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

from prompts import load_prompt

def generate_coverage_report(har_path, dom_path):
    har_data = open(har_path).read()
    dom_html = open(dom_path).read()
    prompt_template = PromptTemplate(
        input_variables=["har_data", "dom_html"],
        template=load_prompt("prompts/coverage_extraction.txt")
    )
    llm = OpenAI(temperature=0.3)
    result = llm(prompt_template.format(har_data=har_data, dom_html=dom_html))
    with open("output/coverage_report.md", "w") as f:
        f.write(result)