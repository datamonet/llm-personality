
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

## 3. Get MBTI and specify MBTI by prompt for GPT3.5 and GPT4o
*(In 'src' folder)*

- `gpt_mbti.ipynb`
  - `mbti_93questions.json`(93 questions) ->  original MBTI result in `llms_mbti93.json`,  which used in `web.py` for visualization , includes **answer details, MBTI type, token and money cost**.
  - `personality_traits.json` -> complete prompts to tested specifying MBTI of LLMs via prompts. Results are in `condition-mbti93.json`.

- `make-mbti60.ipynb`
  - Another mbti test (in their official website) is 60 question with 7 answers each, we build it with `mbti60.txt`, and stored the questionnaire in `mbti_60questions.json`. 
  - We also provide an example to get mbti via 60 question method.

- `functions.py`
  - stores functions to get mbti of llms in different ways.

## 4. Visualization (Streamlit)
*(In 'src' folder)*

Locally run a steamlit page: 

```
streamlit run web.py --server.port 8001
```


## 5. Results
### GPT3.5
#### Personality Type: ENTJ (Commanders)
<div style="text-align: center;">
  <img src="res/ENTJ.png" alt="Celebrities with same MBTI" title="Celebrities with same MBTI" />
  <p><i>(Celebrities who are ENTJ)</i></p>
</div>

#### Overview of the ENTJ

- [ENTJ Personality Type](https://www.16personalities.com/entj-personality)

- People with the ENTJ personality type (Commanders) are natural-born leaders. Embodying the gifts of charisma and confidence, ENTJs project authority in a way that draws crowds together behind a common goal. However, these personalities are also characterized by an often ruthless level of rationality, using their drive, determination, and sharp mind to achieve whatever objectives they’ve set for themselves. Their intensity might sometimes rub people the wrong way, but ultimately, ENTJs take pride in both their work ethic and their impressive level of self-discipline.

#### Usage and Cost Details

- **Total cost for three times testing**: $0.006 USD

### GPT4o
#### Personality Type: INTJ (Logicians)
<div style="text-align: center;">
  <img src="res/INTJ.png" alt="Celebrities with same MBTI" title="Celebrities with same MBTI" />
  <p style="text-align: center;"><i>(Celebrities who are INTJ)</i></p>
</div>


#### Overview of the INTJ 

- [INTJ Personality Type](https://www.16personalities.com/intj-personality)

- People with the INTP personality type (Logicians) pride themselves on their unique perspective and vigorous intellect. They can’t help but puzzle over the mysteries of the universe – which may explain why some of the most influential philosophers and scientists of all time have been INTPs. People with this personality type tend to prefer solitude, as they can easily become immersed in their thoughts when they are left to their own devices. They are also incredibly creative and inventive, and they are not afraid to express their novel ways of thinking or to stand out from the crowd.

#### Usage and Cost Details

- **Total cost for three times testing**: $0.06 USD