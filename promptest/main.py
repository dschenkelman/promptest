import argparse
import os
from datetime import datetime
import yaml
from .tester import test_models

# from https://github.com/yaml/pyyaml/issues/240
def str_presenter(dumper, data):
    """configures yaml for dumping multiline strings
    Ref: https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data"""
    if data.count('\n') > 0:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

def print_results(results):
    for model_name, (_, passes, total) in results.items():
        ratio = passes / total
        print(f"Model: {model_name}, Passes: {passes}, Total: {total}, Passes/Total Ratio: {ratio:.2f}")

def save_test_results(model_name, model_results, passes, total, temperature, max_tokens, template, template_name):
    date = datetime.now().strftime('%Y_%m_%d_%H_%M')
    output_directory = f'prompt_test_results/{date}-{template_name}'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    test_data = {
        'model': model_name,
        'results': model_results,
        'totals': {
            'passes': passes,
            'total': total
        },
        'temperature': temperature,
        'max_tokens': max_tokens,
        'prompt_template': template
    }

    filename = f"{model_name}_test_result.yml"
    file_path = os.path.join(output_directory, filename)

    with open(file_path, 'w') as outfile:
        yaml.dump(test_data, outfile, default_flow_style=None, allow_unicode=True, width=float('inf'), line_break='\n')

def parse_input_files(prompt_path, tests_path):
    with open(prompt_path, 'r') as file:
        prompt_data = yaml.safe_load(file)

    with open(tests_path, 'r') as file:
        tests_data = yaml.safe_load(file)

    return prompt_data, tests_data

def main():
    parser = argparse.ArgumentParser(description='Test LLM models with a given template and inputs.')
    parser.add_argument('--prompt', '-p', type=str, required=True, help='Path to the prompt template YAML file')
    parser.add_argument('--tests', '-t', type=str, required=True, help='Path to the tests YAML file')

    args = parser.parse_args()

    prompt_data, tests_data = parse_input_files(args.prompt, args.tests)
    results = test_models(prompt_data, tests_data)

    template_name = os.path.splitext(os.path.basename(args.prompt))[0]

    for model_name, (model_results, passes, total) in results.items():
        save_test_results(model_name, model_results, passes, total, tests_data['temperature'], tests_data['max_tokens'], prompt_data['template'], template_name)

    print_results(results)
