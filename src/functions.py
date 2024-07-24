import openai, os, json, re
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
openai.api_key = os.getenv('OPENAI_API_KEY')

from openai import OpenAI
client = OpenAI()

# one model, one question, certain temperature. Return an inclination on certain dimension of mbti.
def get_model_answer(model, question, temperature=0.5, add_sys_prompt=''):

    # You can force model to change mbti via 'add_sys_prompt', such as, "Your personality is ????""
    system_prompt = 'You can only anwser one letter, A or B.' + add_sys_prompt 
    
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_format={ "type": "text" },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    
    prompt_tokens = response.usage.prompt_tokens
    input_tokens = response.usage.completion_tokens
    
    if model == 'gpt-3.5-turbo':
        cost = response.usage.total_tokens * 0.5/1000000
    elif model == 'gpt-4o':
        cost = response.usage.total_tokens * 5/1000000
    
    def extract_A_or_B(input_string):
        # 使用正则表达式匹配大写字母A或B
        match = re.search(r'[AB]', input_string)
        if match:
            return match.group()
        else:
            return None
    
    choice = response.choices[0].message.content
    choice = extract_A_or_B(choice)
    return choice, prompt_tokens, input_tokens, cost

# mbti for one model
def get_mbti(model, temperature=0.5, add_sys_prompt='', n=3):
    prompt_tokens =  0
    input_tokens =  0
    cost = 0
    mbti_questions = json.load(
        open('mbti_questions/mbti_93questions.json', 'r', encoding='utf8')
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

    for i in range(n): 
        for q in mbti_questions.values():
            question = q['question']
            res, add_prompt_tokens, add_input_tokens, add_cost = get_model_answer(
                model=model, 
                temperature=temperature, 
                question=question,
                add_sys_prompt=add_sys_prompt
            )
            # print(res)
            mbti_choice = q[res]
            cur_model_score[mbti_choice] += 1
            
            prompt_tokens += add_prompt_tokens
            input_tokens += add_input_tokens
            cost += add_cost
        
    e_or_i = 'E' if cur_model_score['E'] > cur_model_score['I'] else 'I'
    s_or_n = 'S' if cur_model_score['S'] > cur_model_score['N'] else 'N'
    t_or_f = 'T' if cur_model_score['T'] > cur_model_score['F'] else 'F'
    j_or_p = 'J' if cur_model_score['J'] > cur_model_score['P'] else 'P'

    result = {
        'model': model,
        'details': cur_model_score,
        'res': ''.join([e_or_i, s_or_n, t_or_f, j_or_p]),
        "prompt_tokens": prompt_tokens,
        "input_tokens": input_tokens,
        "cost": cost
    }
    
    return(result)

# 60 question mbti
def get_mbti60(user_answers:list):
    if not isinstance(user_answers, list) or len(user_answers) != 60:
        raise ValueError("Input must be a list of length 60.")

    mbti60 = json.load(
        open('mbti_questions/mbti_60questions.json', 'r', encoding='utf8')
    )
    user_answers = [s.capitalize() for s in user_answers]
    
    answer_scores = {
        'Agree': 3,
        'Generally agree': 2,
        'Partially agree': 1,
        'Neither agree nor disagree': 0,
        'Partially disagree': -1,
        'Generally disagree': -2,
        'Disagree': -3
    }

    scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

    for answer, q in zip(user_answers, mbti60.keys()): # record dimension scores of mbti
        tendency = mbti60[q]['tendency']
        score = answer_scores[answer]
        scores[tendency] += score
        
    mbti = '' # calculate mbti results
    mbti += 'E' if scores['E'] >= scores['I'] else 'I'
    mbti += 'N' if scores['N'] >= scores['S'] else 'S'
    mbti += 'F' if scores['F'] >= scores['T'] else 'T'
    mbti += 'J' if scores['J'] >= scores['P'] else 'P'
    
    return mbti, scores

    