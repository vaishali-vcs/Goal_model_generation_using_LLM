# imports needed to run the code in this notebook
import ast  # used for detecting whether generated Python code is valid
import os.path
import time
import openai  # used for calling the OpenAI API
import xml.etree.ElementTree as ET

from utils import (
    load_config,
    load_userstories,
    save_generated_model,
    save_execution_results,
    load_prompt_text
)

color_prefix_by_role = {
    "system": "\033[0m",  # gray
    "user": "\033[0m",  # gray
    "assistant": "\033[92m",  # green
}


def print_messages(messages, color_prefix_by_role=color_prefix_by_role) -> None:
    """Prints messages sent to or from GPT."""
    for message in messages:
        print(f"{message}")


# example of a function that uses a multi-step prompt to create Goal Models
def generate_goal_model(
        stories_to_use: str,  # user stories as a string
        llm_model_name: str,  # name of the LLM that will be used to generate the responses
        prompt_dir: str,  # directory of prompts
        print_text: bool = False,  # optionally prints text; helpful for understanding the function & debugging
        temperature: float = 0.4,  # temperature = 0 can sometimes get stuck in repetitive loops, so we use 0.4
        reruns_if_fail: int = 2,  # if the output code cannot be parsed, this will re-run the function up to N times

) -> str:
    """Outputs a unit test for a given Python function, using a 3-step GPT-3 prompt."""
    # Step 1: Generate the 'Start Prompt'

    start_prompt = load_prompt_text(prompt_dir, "Start_Prompt.txt")

    format_text = f"""
    <?xml version='1.0' encoding='ISO-8859-1'?>
    <grl-catalog catalog-name="URNspec" description="" author="vaish">
        <element-def>
            <intentional-element id="72" name="Car objects" description="" type="Ressource" decompositiontype="And"/>
            <intentional-element id="80" name="Easy to use" description="" type="Softgoal" decompositiontype="And"/>
            <intentional-element id="82" name="Realistic simulation" description="" type="Softgoal" decompositiontype="And"/>
            <intentional-element id="84" name="Simple design" description="" type="Softgoal" decompositiontype="And"/>
            <intentional-element id="88" name="Generate cars" description="" type="Goal" decompositiontype="And"/>
            <intentional-element id="96" name="Create new cars" description="" type="Task" decompositiontype="And"/>
            <intentional-element id="98" name="Keep same cars" description="" type="Task" decompositiontype="And"/>
        </element-def>
        <link-def>
            <contribution name="Contribution105" description="" srcid="96" destid="82" contributiontype="Unknown" quantitativeContribution="0" correlation="false"/>
            <contribution name="Contribution106" description="" srcid="96" destid="84" contributiontype="Unknown" quantitativeContribution="0" correlation="false"/>
            <decomposition name="Decomposition111" description="" srcid="96" destid="88"/>
            <decomposition name="Decomposition114" description="" srcid="98" destid="88"/>
            <dependency name="Dependency116" description="" dependerid="88" dependeeid="72"/>
        </link-def>
        <actor-def>
            <actor id="11" name="Traffic Simulator" description=""/>
        </actor-def>
        <actor-IE-link-def>
            <actorContIE actor="11" ie="72"/>
            <actorContIE actor="11" ie="80"/>
            <actorContIE actor="11" ie="82"/>
            <actorContIE actor="11" ie="84"/>
            <actorContIE actor="11" ie="88"/>
            <actorContIE actor="11" ie="96"/>
            <actorContIE actor="11" ie="98"/>
        </actor-IE-link-def>
    </grl-catalog>
    """

    # create a markdown-formatted message that sets the role of the GPT
    start_system_message = {
        "role": "system",
        "content": start_prompt,
    }
    start_user_message = {
        "role": "user",
        "content": f""" You will be provided with user story delimited by triple quotes. Create a Goal-oriented Requirement 
Language (GRL) Model for the given user story. Re-write the answer in the format delimited by triple back ticks. 
Generate unique values for 'id' attribute. Do not forget to include as many soft goals, tasks and resources as possible. 
You should also break down goals that are at higher level of abstraction to lower level goals and tasks. Do the same for soft goals, as well.
Provide a confidence score for your answer. \


\"\"\"{stories_to_use}\"\"\"

```{format_text}```
""",
    }
    start_messages = [start_system_message, start_user_message]
    if print_text:
        print_messages(start_messages)

    start = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=start_messages,
        temperature=temperature
    )

    start_response = start.choices[0].message.content

    if print_text:
        print_messages(start_response)

    # append the previous question and the response
    start_assistant_message = {"role": "assistant", "content": start_response}

    # introduce delay of 1 minute before the next API Call
    time.sleep(60)

    # Step 2.1: Identify Actors in the stories
    actors_prompt = load_prompt_text(prompt_dir, "IdentifyActors_Prompt.txt") + f"```{format_text}``` "
    # Asks GPT to plan out cases the units tests should cover, formatted as a bullet list
    actors_user_message = {
        "role": "user",
        "content": actors_prompt,
    }
    plan_messages = [
        start_system_message,
        start_user_message,
        start_assistant_message,
        actors_user_message,
    ]
    if print_text:
        print_messages([actors_user_message])

    actors_response = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=plan_messages,
        temperature=temperature
    )

    actors = actors_response.choices[0].message.content

    if print_text:
        print_messages(actors)

    actor_assistant_message = {"role": "assistant", "content": actors}

    # introduce delay of 1 minute before the next API Call
    time.sleep(60)

    # Step 2.2: Identify Soft Goals, Goals and Resources
    goals_prompt = load_prompt_text(prompt_dir, "IdentifyGoals_Prompt.txt")+ f"```{format_text}``` "
    goals_user_message = {
        "role": "user",
        "content": goals_prompt,
    }
    plan_messages = [
        start_system_message,
        start_user_message,
        start_assistant_message,
        actors_user_message,
        actor_assistant_message,
        goals_user_message,
    ]
    if print_text:
        print_messages([goals_user_message])

    goals = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=plan_messages,
        temperature=temperature
    )

    goals_message = goals.choices[0].message.content

    if print_text:
        print_messages(goals_message)

    goals_assistant_message = {"role": "assistant", "content": goals_message}

    # introduce delay of 1 minute before the next API Call
    time.sleep(60)

    # Step 2.3: Identify Tasks
    tasks_prompt = load_prompt_text(prompt_dir, "IdentifyTasks_Prompt.txt")+ f"```{format_text}``` "

    tasks_user_message = {
        "role": "user",
        "content": tasks_prompt,
    }

    plan_messages = [
        start_system_message,
        start_user_message,
        start_assistant_message,
        actors_user_message,
        actor_assistant_message,
        goals_user_message,
        goals_assistant_message,
        tasks_user_message
    ]

    if print_text:
        print_messages([tasks_user_message])

    tasks = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=plan_messages,
        temperature=temperature
    )
    tasks_message = tasks.choices[0].message.content

    if print_text:
        print_messages(tasks_message)
    tasks_assistant_message = {"role": "assistant", "content": tasks_message}

    # introduce delay of 1 minute before the next API Call
    time.sleep(60)

    # Step 2.4: Identify Means-End Links
    means_end_prompt = load_prompt_text(prompt_dir, "IdentifyMeansEndLinks_Prompt.txt")+ f"```{format_text}``` "

    meansend_user_message = {
        "role": "user",
        "content": means_end_prompt,
    }

    plan_messages = [
        start_system_message,
        start_user_message,
        start_assistant_message,
        actors_user_message,
        actor_assistant_message,
        goals_user_message,
        goals_assistant_message,
        tasks_user_message,
        tasks_assistant_message,
        meansend_user_message
    ]

    if print_text:
        print_messages([meansend_user_message])

    meansend = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=plan_messages,
        temperature=temperature
    )
    meansend_message = meansend.choices[0].message.content

    if print_text:
        print_messages(meansend_message)
    meansend_assistant_message = {"role": "assistant", "content": meansend_message}

    # introduce delay of 1 minute before the next API Call
    time.sleep(60)

    # Step 2.5: Identify Decomposition Links
    decomposition_prompt = load_prompt_text(prompt_dir, "IdentifyDecompositionLinks_Prompt.txt")+ f"```{format_text}``` "

    decomposition_user_message = {
        "role": "user",
        "content": decomposition_prompt,
    }

    plan_messages = [
        start_system_message,
        start_user_message,
        start_assistant_message,
        actors_user_message,
        actor_assistant_message,
        goals_user_message,
        goals_assistant_message,
        tasks_user_message,
        tasks_assistant_message,
        meansend_user_message,
        meansend_assistant_message,
        decomposition_user_message
    ]

    if print_text:
        print_messages([decomposition_user_message])

    decompositions = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=plan_messages,
        temperature=temperature
    )
    decompositions_message = decompositions.choices[0].message.content

    if print_text:
        print_messages(decompositions_message)
    decompositions_assistant_message = {"role": "assistant", "content": decompositions_message}

    # Step 2.6: Identify Contribution Links
    contribution_prompt = load_prompt_text(prompt_dir, "IdentifyContributionLinks_Prompt.txt")+ f"```{format_text}``` "

    contribution_user_message = {
        "role": "user",
        "content": contribution_prompt,
    }

    plan_messages = [
        start_system_message,
        start_user_message,
        start_assistant_message,
        actors_user_message,
        actor_assistant_message,
        goals_user_message,
        goals_assistant_message,
        tasks_user_message,
        tasks_assistant_message,
        meansend_user_message,
        meansend_assistant_message,
        decomposition_user_message,
        decompositions_assistant_message,
        contribution_user_message
    ]

    if print_text:
        print_messages([contribution_user_message])

    contributions = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=plan_messages,
        temperature=temperature
    )
    contributions_message = contributions.choices[0].message.content

    if print_text:
        print_messages(contributions_message)
    contributions_assistant_message = {"role": "assistant", "content":  contributions_message}

    # Step 2.7: Identify Dependency Links
    dependency_prompt = load_prompt_text(prompt_dir, "IdentifyDependencyLinks_Prompt.txt")+ f"```{format_text}``` "

    dependency_user_message = {
        "role": "user",
        "content": dependency_prompt,
    }

    plan_messages = [
        start_system_message,
        start_user_message,
        start_assistant_message,
        actors_user_message,
        actor_assistant_message,
        goals_user_message,
        goals_assistant_message,
        tasks_user_message,
        tasks_assistant_message,
        meansend_user_message,
        meansend_assistant_message,
        decomposition_user_message,
        decompositions_assistant_message,
        contribution_user_message,
        contributions_assistant_message,
        dependency_user_message
    ]

    if print_text:
        print_messages([dependency_user_message])

    dependencies = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=plan_messages,
        temperature=temperature
    )
    final_goal_model = dependencies.choices[0].message.content

    if print_text:
        print_messages(final_goal_model)

    # the below code validates the generated XML. If malformed XML is generated then begin the generation process
    try:
        # Parse the XML document
        tree = ET.fromstring(final_goal_model)

    except SyntaxError as e:
        print(f"Syntax error in generated final_goal_model: {e}")
        if reruns_if_fail > 0:
            print("Rerunning...")

            return generate_goal_model(
                    stories_to_use,
                    llm_model_name,
                    prompt_dir,
                    reruns_if_fail= reruns_if_fail - 1)

    return final_goal_model


def main():
    generation_status = []

    config = load_config("config.json")

    set_stories = load_userstories(config["INPUT_DIRECTORY"])
    story_no = 1
    for stories in set_stories:
        generation_status.append("Success!")

        goal_model = generate_goal_model(stories_to_use=stories, llm_model_name = "gpt-3.5-turbo",prompt_dir = config["PROMPTS_DIRECTORY"], print_text = False)

        # save the goal model generated by LLM
        save_generated_model(config["OUTPUT_DIRECTORY"], f"Story{story_no}.grl", goal_model)

        story_no += 1
    # save the results of the current execution
    save_execution_results(os.path.join(config["BASE_DIRECTORY"], config["OUTPUT_DIRECTORY"]),
                           "generation_status.csv",
                           zip([f"Story{i}" for i in set_stories], generation_status))


if __name__ == "__main__":
    main()
