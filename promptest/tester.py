import re
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)
import yaml

CHAT_MODELS=["gpt-4", "gpt-4-0314", "gpt-4-32k", "gpt-4-32k-0314", "gpt-3.5-turbo", "gpt-3.5-turbo-0301"]

def _compare_output(output, expected_output):
    if expected_output['type'] == 'regex':
        pattern = re.compile(expected_output['value'])
        return pattern.match(output) is not None, None
    elif expected_output['type'] == 'string':
        return output == expected_output['value'], None
    elif expected_output['type'] == 'yaml':
        try:
            output_yaml = yaml.safe_load(output)
            expected_yaml = yaml.safe_load(expected_output['value'])
            return output_yaml == expected_yaml, None
        except yaml.YAMLError:
            return False
    elif expected_output['type'] == 'prompt':
        model = expected_output['model']
        llm = OpenAI(model_name=model, temperature=0, max_tokens=1800)
        out_value = expected_output['value']

        params = { 'input_text': output, 'conditions': out_value['conditions'] }
        current_file_path = os.path.abspath(__file__)
        current_dir_path = os.path.dirname(current_file_path)

        with open(os.path.join(current_dir_path, 'templates/conditions_on_text.yml'), 'r') as file:
            template = file.read()

        if model in CHAT_MODELS:
            llm = ChatOpenAI(model_name=model, temperature=0, max_tokens=1800)
            prompt_template = ChatPromptTemplate.from_messages([HumanMessagePromptTemplate.from_template(template=template)])
        else:
            llm = OpenAI(model_name=model, temperature=0, max_tokens=1800)
            prompt_template =  PromptTemplate(template=template, input_variables=['input_text', 'conditions'])

        llm_chain = LLMChain(llm=llm, prompt=prompt_template, output_key='validation_result')

        validation_result = llm_chain.predict(**params).strip()

        try:
            validation_result_yaml = yaml.safe_load(validation_result)
            overall_pass = validation_result_yaml.get('pass', False)
            return overall_pass, validation_result_yaml
        except yaml.YAMLError:
            return False
    else:
        return False

def test_models(prompt_data, tests_data):
    template = prompt_data['template']
    input_variables = prompt_data['input_variables']
    output_key = prompt_data['output_key']

    tests = tests_data['tests']
    model_names = tests_data['model_names']
    temperature = tests_data['temperature']
    max_tokens = tests_data['max_tokens']

    results = {}

    for model_name in model_names:
        total = 0
        passes = 0
        model_results = []

        if model_name in CHAT_MODELS:
            llm = ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens)
            prompt_template = ChatPromptTemplate.from_messages([HumanMessagePromptTemplate.from_template(template=template)])
        else:
            llm = OpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens)
            prompt_template = PromptTemplate(template=template, input_variables=input_variables)

        llm_chain = LLMChain(llm=llm, prompt=prompt_template, output_key=output_key)

        for item in tests:
            variables = item['variables']
            expected_output = item['expected_output']

            result = llm_chain.predict(**variables).strip()

            comparison_result, extra_data = _compare_output(result, expected_output)

            if comparison_result:
                passes += 1

            test_result = {
                'inputs': variables,
                'output': result,
                'comparison_result': comparison_result,
                'extra_data': extra_data
            }
            model_results.append(test_result)

            total += 1

        results[model_name] = (model_results, passes, total)

    return results
