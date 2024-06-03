# Goal Model Extraction from User Stories Using Large Language Models

This project consists of the code, the inputs, and outputs used in the paper titled "Goal Model Extraction from User Stories Using Large Language Models". 
This paper presents early research proposing a technique using Large Language Models (LLMs), like GPT-4, to automatically generate goal models from user stories. The approach
employs Iterative Prompt Engineering to guide the LLM in extracting intentional elements and generating XML representations using the Goal-oriented Requirements Language (GRL), visualized with the jUCMNav tool.

## Repository Structure
1. 'Inputs' folder consists of the user stories that were used to evaluate the approach.
2. 'Prompts' folder consists of the textual prompts used to generate responses.
3. 'Outputs' folder consists of responses from GPT-4.
4. 'API_Key.txt' file consists of the OPENAI License Key.
5. 'GPT4_goalmodel_generation.py' consists of the driver code.

## Evaluation
To evaluate our approach, ten GRL models were randomly selected from the literature, where these models are well-validated and commonly used within the realm of goal
modeling literature. The first GRL model is related to the requirements of traffic simulator software and is found in [1]. Two GRL models of waste management software and one
related to human resources software are taken from [2]. One GRL model of a hospital’s Wait Time Estimation System and one belonging to a wireless telephony company are adopted from [3] and [4], respectively. Lastly, one GRL model for an online shopping business and three models related to a none-for-profit organization that counsels youth over the phone are taken from [5] and [6], respectively. 

The data adopted from the literature include GRL models and snippets of requirements that were not in the format of user stories. Therefore, the authors transformed
them into the format of the user story. This strategy of data acquisition helps to evaluate the methodology independently without relying on domain experts to conduct an acceptability test.

## How to install?
Following are steps to be followed:
1. Create a Virtual Environment.
2. Install Python 3.9, Pandas, and Tensorflow.
3. PIP Install openai using the below command  <br />
   *pip install openai*
5. Clone this project.
6. Procure an OPENAI API Key.
7. Paste the key in API_Key.txt file without any double/single quotes.
8. Run the script - GPT4_goalmodel_generation.py

## How to tweak this project for your own uses?
Since this is a boilerplate version of the project, it has been tested only on User Stories as the input. I'd encourage you to clone and rename this project to test it on other forms of requirements.

## Find a bug?
If you found an issue or would like to submit an improvement to this project, please submit an issue using the 'Issues' tab. If you would like to submit a PR with a fix, reference the issue you created. 

## References
[1] M. van Zee, F. Bex, and S. Ghanavati, “Rationalgrl: A framework for argumentation and goal modeling,” Argument & Computation, vol. 12,
pp. 191–245, 2021.
[2] T. Gunes and F. B. Aydemir, “Automated goal model extraction from user stories using nlp,” pp. 382–387, 2020.
[3] M. Baslyman, B. Almoaber, D. Amyot, and E. M. Bouattane, “Activitybased process integration in healthcare with the user requirements
notation,” 05 2017, pp. 151–169.
[4] D. Amyot, “Introduction to the user requirements notation: learning by example,” Computer Networks, vol. 42, no. 3, pp. 285–301, 2003.
[5] G. v. Bochmann, “Goal modeling and grl,” https://www.site.uottawa.ca/∼bochmann/SEG3101/Notes/SEG3101-ch3-5%20-%20Goal%20modeling%20-%20GRL.pdf, 2009, accessed: 2023–12-06.
[6] J. Horkoff and E. Yu, “Interactive goal model analysis for early requirements engineering,” Requirements Engineering, vol. 21, no. 1, pp. 29–61, 2016. [Online]. Available: https://doi.org/10.1007/s00766-014-0209-8
