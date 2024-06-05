import json
import os
import pandas as pd
import openai


def load_config(config_file: str) -> dict:
    """
    Loads the JSON configuration and sets the OpenAI API key.
    @param config_file:  Path to the JSON configuration file.
    @returns config: dictionary of the parsed configuration
    """
    with open(config_file) as json_file:
        config = json.load(json_file)
    # sets the OpenAI key
    openai.api_key = config["OPEN_AI_KEY"]
    return config


def load_userstories(input_dir: str) -> list:
    stories = []

    # iterate over files in
    # that directory
    for filename in os.listdir(input_dir):
        stories_file = os.path.join(input_dir, filename)

        # checking if it is a file
        if os.path.isfile(stories_file):

            # Opening file
            file1 = open(stories_file, 'r')
            file_content = ''

            for line in file1:
                file_content = file_content + line

            # Closing files
            file1.close()

        stories.append(file_content)
    return stories


def save_generated_model(output_dir: str, output_filename: str, contents: str) -> None:
    with open(os.path.join(output_dir,
                           output_filename), 'w') as generated_goalmodel:
        generated_goalmodel.write(contents)


def save_execution_results(output_dir: str, output_filename: str, results_lst: list) -> None:
    # Calling DataFrame constructor on the zipped lists, with columns specified
    results_df = pd.DataFrame(results_lst,
                              columns=['Stories', 'Status'])
    # save the contents as a csv
    results_df.to_csv(os.path.join(output_dir, output_filename))


def load_prompt_text(file_dir:str, textfile:str)->str:
    # checking if it is a file
    # Opening file
    file1 = open(os.path.abspath(os.path.join(file_dir,
                           textfile)))
    prompt_content = ''

    for line in file1:
        prompt_content = prompt_content + line

    # Closing files
    file1.close()

    return prompt_content
