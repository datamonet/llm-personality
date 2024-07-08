#!/usr/bin/env python
# coding: utf-8

# In[2]:


import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()  # take environment variables from .env.
openai.api_key = os.getenv('OPENAI_API_KEY')

from openai import OpenAI
client = OpenAI()


# In[3]:


cost_info = {
    'prompt_tokens': 0,
    'input_tokens': 0,
    'cost': 0
}


# In[4]:


# one model, one question, certain temperature
def get_model_answer(model, temperature, question):
    system_prompt = 'You can only anwser one letter, A or B'
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_format={ "type": "text" },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    
    cost_info['prompt_tokens'] += response.usage.prompt_tokens
    cost_info['input_tokens'] += response.usage.completion_tokens
    
    if model == 'gpt-3.5-turbo':
        cost_info['cost'] += response.usage.total_tokens * 0.5/1000000
    elif model == 'gpt-4o':
        cost_info['cost'] += response.usage.total_tokens * 5/1000000
    
    return response.choices[0].message.content


# In[5]:


# mbti for one model
def get_mbti(model, temperature=0.5):
    mbti_questions = json.load(
        open('mbti_questions.json', 'r', encoding='utf8')
    )

    cur_model_score = {
            'E': 0,
            'I': 0,
            'S': 0,
            'N': 0,
            'T': 0,
            'F': 0,
            'J': 0,
            'P': 0
        }

    for i in range(3): 
        for q in mbti_questions.values():
            question = q['question']
            res = get_model_answer(
                model=model, 
                temperature=temperature, 
                question=question+'You can only answer A or B, only one letter'
            )
            # print(res)
            mbti_choice = q[res]
            cur_model_score[mbti_choice] += 1
        
    e_or_i = 'E' if cur_model_score['E'] > cur_model_score['I'] else 'I'
    s_or_n = 'S' if cur_model_score['S'] > cur_model_score['N'] else 'N'
    t_or_f = 'T' if cur_model_score['T'] > cur_model_score['F'] else 'F'
    j_or_p = 'J' if cur_model_score['J'] > cur_model_score['P'] else 'P'

    result = {
        'model': model,
        'details': cur_model_score,
        'res': ''.join([e_or_i, s_or_n, t_or_f, j_or_p])
    }
    
    return(result)
    


# In[17]:


# gpt3.5 mbti and api cost(per round) 
cost_info = {
    'prompt_tokens': 0,
    'input_tokens': 0,
    'cost': 0
}

result_gpt3 = get_mbti(model='gpt-3.5-turbo')
result_gpt3 = result_gpt3 | cost_info
print(json.dumps(result_gpt3))

# In[13]:


# Save result of two models using a dict
SAVE_PATH = 'llms_mbti.json'

llms_mbti = {}
llms_mbti["gpt-3.5"] = result_gpt3


# In[14]:


# gpt4o mbti and api cost(per round)
cost_info = {
    'prompt_tokens': 0,
    'input_tokens': 0,
    'cost': 0
}

result_gpt4o = get_mbti(model='gpt-4o')
result_gpt4o = result_gpt4o | cost_info
print(json.dumps(result_gpt4o))


# In[15]:


llms_mbti["gpt-4o"] = result_gpt4o


# In[19]:


# Save the dictionary as a JSON object to a file
with open(SAVE_PATH, 'w', encoding='utf8') as json_file:
    json.dump(llms_mbti, json_file, indent=4)  # indent=4 for pretty-printing


# ---

# ## Mbti for GPT3.5 and cost per round
# - **Mbti details**
#   - model: gpt-3.5-turbo, 
#   - details(3 times per questions): {E: 38, I: 25, S: 23, N: 58, T: 35, F: 34, J: 54, P: 12}, 
#   - res: [ENTJ](https://www.16personalities.com/entj-personality)  
# - **Cost info per round**
#   - prompt_tokens: 20304, 
#   - input_tokens: 279, 
#   - cost: 0.0102915

# ## Mbti for GPT4o and cost per round
# 
# - **Mbti details**
#   - model: gpt-4o, 
#   - details: {E: 18, I: 45, S: 24, N: 57, T: 36, F: 33, J: 57, P: 9}, 
#   - res: [INTJ](https://www.16personalities.com/intj-personality)
# - **Cost info per round**
#   - prompt_tokens: 16974, 
#   - input_tokens: 279, 
#   - cost: 0.08626499999999994

# 
