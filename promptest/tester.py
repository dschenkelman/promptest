import re
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import yaml

def _compare_output(output, expected_output):
    if expected_output['type'] == 'regex':
        pattern = re.compile(expected_output['value'])
        return pattern.match(output) is not None
    elif expected_output['type'] == 'string':
        return output == expected_output['value']
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

        llm = OpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens)

        prompt_template = PromptTemplate(template=template, input_variables=input_variables)
        llm_chain = LLMChain(llm=llm, prompt=prompt_template, output_key=output_key)

        for item in tests:
            variables = item['variables']
            expected_output = item['expected_output']

            result = llm_chain.predict(**variables).strip()

            comparison_result = _compare_output(result, expected_output)

            if comparison_result:
                passes += 1

            test_result = {
                'inputs': variables,
                'output': result,
                'comparison_result': comparison_result,
            }
            model_results.append(test_result)

            total += 1

        results[model_name] = (model_results, passes, total)

    return results
