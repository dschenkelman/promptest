# promptest
`promptest` is a command-line tool to test prompts with language models (LLMs).

## Installation
To install `promptest`, run the following command:
```bash
pip install promptest
```

## Usage

Make the OpenAI API key available as an environment variable:
```bash
export OPENAI_API_KEY=sk-...
```

To use `promptest`, run the following command:
```bash
promptest --prompt /path/to/prompt.yaml --inputs /path/to/inputs.yaml
```

Here, `/path/to/prompt.yaml` should be the path to a YAML file containing the template for your LLM, and `/path/to/inputs.yaml` should be the path to a YAML file containing the inputs for your tests.

For more information on the command line arguments that `promptest` supports, run:
```bash
promptest --help
```


## Example
Here is an example of how to use `promptest` to test an LLM model:

1. Create a YAML file `prompt.yaml` containing the template for your LLM:
    ```yaml
    template: |
        Provide the longest word in terms of characters in an input piece of text.
        Only provide the word, no other text.
        Provide the word exactly as written in the text, do not modify it, capitalize it, etc.

        The text is:
        {text}
    input_variables:
        - text
    output_key: longest_word
    ```

2. Create a YAML file `inputs.yaml` containing the inputs for your tests:
    ```yaml
    model_names:
	- text-davinci-003
    temperature: 0
    max_tokens: 30
    tests:
        - variables:
            text: "the longest word in this text is longest"
        expected_output:
            type: "string"
            value: "longest"
        - variables:
            text: "the longest word in this text is confusing"
        expected_output:
            type: "string"
            value: "confusing"
    ```

3. Run the following command to test the prompt templates:
```bash
promptest --prompt prompt.yaml --tests tests.yaml
```

This will output detailed results for each model, including the number of test cases passed and the pass ratio.

When you run `promptest`, the tool will execute tests for each LLM model specified in the `tests.yaml` file. For each model, `promptest` will run the tests and output the results to the console. In addition to the console output, `promptest` will also create a file containing the detailed test results.

The file will be named model_name_test_result.yml, where model_name is the name of the LLM model being tested (e.g., gpt, gpt2, etc.). The file will be written to a directory named prompt_test_results in the current working directory. The directory will be named with a timestamp and the name of the template file being used, in the following format:
```
prompt_test_results/YYYY_MM_DD_HH_MM_template_name/
```

The YAML file will contain the following information:

Yes, you're correct. I apologize for the mistake in my previous response. The output directory will include the date and time when the test was run, as well as the name of the template file being used. Here's an updated markdown block:

When you run promptest, the tool will execute tests for each LLM model specified in the inputs.yaml file. For each model, promptest will run the tests and output the results to the console. In addition to the console output, promptest will also create a file containing the detailed test results.

The file will be named model_name_test_result.yml, where model_name is the name of the LLM model being tested (e.g., gpt, gpt2, etc.). The file will be written to a directory named prompt_test_results in the current working directory. The directory will be named with a timestamp and the name of the template file being used.

The YAML file will contain the following information:

```yaml
max_tokens: 30
model: text-davinci-003
prompt_template: |
  Provide the longest word in terms of characters in an input piece of text.
  Only provide the word, no other text.
  Provide the word exactly as written in the text, do not modify it, capitalize it, etc.

  The text is:
  {text}
results:
- comparison_result: true
  inputs: {text: the longest word in this text is longest}
  output: longest
- comparison_result: true
  inputs: {text: the longest word in this text is confusing}
  output: confusing
temperature: 0
totals: {passes: 2, total: 2}
```

## License

`promptest` is released under the [MIT License](https://opensource.org/licenses/MIT).
