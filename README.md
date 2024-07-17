
# LLMs_MBTI👩‍💼👨‍💻👨‍💼👩‍🎤🕵️‍♀️
This repo test MBTI for *gpt3.5* and *gpt4o*.   

The MBTI analyzes personality on 4 dimensions, each containing 2 opposing preferences:   

1. **Extraversion E-Introversion I:** representing the different sources of energy in each person.
2. **Sensing S - Intuition N:** representing different brain preferences for sensing.
3. **Thinking T - Feeling F:** Representing different brain preferences for judgment.
4. **judgment J - perception P:** whether perception or judgment plays a dominant role in people's adaptation to the external environment.

We test each [MBTI question](./mbti_questions.json) for each language model for 3 times and get their preferences on 4 dimensions according to the number of answers with different preferences for each dimension. *[Here is a streamlit web page of result](https://derekwang2002-streamlit-repo-web-gyx7yx.streamlit.app/)*

[You can see more llm-personality research at here.](https://quilt-trouble-855.notion.site/LLM-MBTI-Papers-1222a8ae851045959403e4628804129a?pvs=74)

## 1. Install

```
pip install -r requirements.txt
```

## 2. Store your keys

In order to hide sensitive information (API keys), you should store your keys in `.env` file (which should be ignored by git) like:

```
OPENAI_API_KEY=sk-xxxxxxx
```

And include in your code like:

```python
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

openai.api_key = os.getenv('OPENAI_API_KEY')
```

If you don't have `dotenv`, install first:

```
pip install python-dotenv
```

## 3. Get MBTI for GPT3.5 and GPT4o
*(In 'srr' folder)*

Use `mbti_questions.json` in `gpt-api-starter.ipynb`, we get result in `llms_mbti.json`, includes **answer details, MBTI type, token and money cost**.

Then, `llms_mbti.json` can be further used in `web.py` for visualization.

## 4. Visualization (Streamlit)
*(In 'src' folder)*

Locally run a steamlit page: 

```
streamlit run web.py --server.port 8001
```


## 5. Results
### GPT3.5
#### Personality Type: ENTJ Commander
<div style="text-align: center;">
  <img src="res/ENFJ.png" alt="Celebrities with same MBTI" title="Celebrities with same MBTI" />
  <p><i>Celebrities who are ENFJ</i></p>
</div>

#### Overview of the ENTJ

[ENFJ Personality Type](https://www.16personalities.com/enfj-personality)

ENFJ (Protagonist) is a personality type with the Extraverted, Intuitive, Feeling, and Judging traits. These warm, forthright types love helping others, and they tend to have strong ideas and values. They back their perspective with the creative energy to achieve their goals.

#### Usage and Cost Details

- **Total cost for three times testing**: $0.010 USD

### GPT4o
#### Personality Type: INTJ Architect
<div style="text-align: center;">
  <img src="res/INFJ.png" alt="Celebrities with same MBTI" title="Celebrities with same MBTI" />
  <p style="text-align: center;"><i>Celebrities who are INTJ</i></p>
</div>


#### Overview of the INTJ 

[INFJ Personality Type](https://www.16personalities.com/infj-personality)

INFJ (Advocate) is a personality type with the Introverted, Intuitive, Feeling, and Judging traits. They tend to approach life with deep thoughtfulness and imagination. Their inner vision, personal values, and a quiet, principled version of humanism guide them in all things.

#### Usage and Cost Details

- **Total cost for three times testing**: $0.084 USD