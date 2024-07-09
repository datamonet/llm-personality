# !/usr/bin/env python3

import json

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="LLMs MBTI"
)

st.markdown(
    "<h1 style='text-align: center;'>🧸 LLMs MBTI</h1>", 
    unsafe_allow_html=True
)

MBTI_DESCRIPTIONS = {
    'ISTJ': {
        'short_desc': 'Introversion / Sensing / Thinking / Judging',
        'features': '1. Serious and quiet, achieving success through concentration and reliable commitment.  \n2. Practical, orderly, realistic, logical, true, and reliable.  \n3. Very attentive and happy to have good organization and order in all things (work, home, life).  \n4. Responsible.  \n5. Make decisions based on established results and are steadfast in the face of obstacles and gossip.  \n6. Value tradition and loyalty.  \n7. Traditional thinkers or managers.'
    },
    'ISFJ': {
        'short_desc': 'Introversion / Sensing / Feeling / Judging',
        'features': '1. Quiet, kind, responsible, and conscientious.  \n2. Diligent and committed in their actions.  \n3. High stability, often the stabilizing force in projects or teams.  \n4. Willing to work hard, endure hardships, and strive for accuracy.  \n5. Usually not interested in technology. Patient with detailed tasks.  \n6. Loyal, considerate, intellectual, and concerned with the feelings of others.  \n7. Dedicated to creating an orderly and harmonious work and family environment.'
    },
    'INFJ': {
        'short_desc': 'Introversion / Intuition / Feeling / Judging',
        'features': '1. Successful due to perseverance, creativity, and a strong sense of purpose.  \n2. Puts maximum effort into their work.  \n3. Quietly strong, sincere, and genuinely caring about others.  \n4. Respected for their principles.  \n5. Respected and followed for presenting a clear vision that benefits the public.  \n6. Pursue the meaning and connections of ideas, relationships, and material possessions.  \n7. Wants to understand what motivates others and has insights into others.  \n8. Honest and firmly believes in their values.  \n9. Organized and decisive in carrying out their vision.'
    },
    'INTJ': {
        'short_desc': 'Introversion / Intuition / Thinking / Judging',
        'features': '1. Strong drive and intention to achieve goals and ideas—stubborn and determined.  \n2. Has a grand vision and can quickly identify meaningful patterns among external events.  \n3. Capable of planning and completing tasks efficiently in their duties.  \n4. Skeptical, critical, independent, decisive, and holds high standards for competence and performance.'
    },
    'ISTP': {
        'short_desc': 'Introversion / Sensing / Thinking / Perceiving',
        'features': '1. Calm observer—quiet, adaptable, flexible, and curious with an unbiased curiosity and unexpected original humor.  \n2. Interested in exploring the reasons and effects of technical issues, how things work, and uses logical principles to construct facts, valuing efficiency.  \n3. Good at grasping the core of problems and finding solutions.  \n4. Analyzes the reasons for success and can quickly identify the core practical issues from a large amount of data.'
    },
    'ISFP': {
        'short_desc': 'Introversion / Sensing / Feeling / Perceiving',
        'features': '1. Shy, peaceful, kind, sensitive, and modest in their actions.  \n2. Likes to avoid conflicts and does not impose their views or values on others.  \n3. Not interested in leading but often loyal followers.  \n4. Works without urgency, content with the status quo, and not driven by results.  \n5. Likes to have their own space and follow their own schedule.'
    },
    'INFP': {
        'short_desc': 'Introversion / Intuition / Feeling / Perceiving',
        'features': '1. Quiet observer, idealistic and loyal to their values and important people.  \n2. Wants external life to align with inner values.  \n3. Curious and quick to see opportunities, often a catalyst for developing ideas.  \n4. Flexible, adaptable, and resilient unless their values are violated.  \n5. Eager to understand and develop others potential. Focuses intensely on their tasks.  \n6. Not very concerned with circumstances or possessions.  \n7. Adaptable and flexible unless their values are threatened.'
    },
    'INTP': {
        'short_desc': 'Introversion / Intuition / Thinking / Perceiving',
        'features': '1. Quiet, reserved, flexible, and adaptable.  \n2. Particularly fond of pursuing theories and scientific principles.  \n3. Used to solving problems with logic and analysis—problem solvers.  \n4. Most interested in creative matters and specific work, not much interested in gatherings and chit-chat.  \n5. Pursues a career that allows them to follow their strong personal interests.  \n6. Seeks logical explanations for matters of interest.'
    },
    'ESTJ': {
        'short_desc': 'Extraversion / Sensing / Thinking / Judging',
        'features': '1. Practical, realistic, and fact-oriented, with entrepreneurial or technical talents.  \n2. Dislikes abstract theories; prefers learning immediately applicable principles.  \n3. Likes to organize and manage activities, focusing on the most efficient way to achieve results.  \n4. Decisive, detail-oriented, and quick to make decisions—excellent administrators.  \n5. May overlook others\' feelings.  \n6. Prefers leadership roles or corporate management.'
    },
    'ESFJ': {
        'short_desc': 'Extraversion / Sensing / Feeling / Judging',
        'features': '1. Sincere, talkative, cooperative, popular, and fair-minded—natural collaborators and active group members.  \n2. Values harmony and excels at creating it.  \n3. Often engages in activities beneficial to others.  \n4. Better work performance with encouragement and praise.  \n5. Most interested in matters that directly and tangibly affect people\'s lives.  \n6. Likes to work with others to complete tasks accurately and on time.'
    },
    'ENFJ': {
        'short_desc': 'Extraversion / Intuition / Feeling / Judging',
        'features': '1. Enthusiastic, empathetic, and responsible—leaders who encourage others.  \n2. Genuinely concerned about others\' thoughts and desires, and addresses them with sincerity.  \n3. Skillfully and pleasantly leads group discussions or presentations.  \n4. Sociable, popular, and empathetic.  \n5. Sensitive to praise and criticism.  \n6. Likes to guide others and helps them or groups reach their potential.'
    },
    'ENTJ': {
        'short_desc': 'Extraversion / Intuition / Thinking / Judging',
        'features': '1. Frank, decisive activity leaders.  \n2. Skilled at developing and implementing broad systems to solve organizational problems.  \n3. Expert in meaningful and intelligent discussions, such as public speaking.  \n4. Enjoys continually absorbing new knowledge and can open information channels widely.  \n5. May become overly confident and strongly express their ideas.  \n6. Likes long-term planning and goal setting.'
    },
    'ESTP': {
        'short_desc': 'Extraversion / Sensing / Thinking / Perceiving',
        'features': '1. Skilled at solving on-the-spot problems—problem solvers.  \n2. Enjoys doing things and takes pleasure in the process.  \n3. Inclined to technical matters and sports, making friends easily.  \n4. Adaptable, tolerant, practical; invests effort in work that quickly shows results.  \n5. Dislikes lengthy explanations and theories.'
    },
    'ESFP': {
        'short_desc': 'Extraversion / Sensing / Feeling / Perceiving',
        'features': '1. Extraverted, kind, accepting, enjoys sharing joy with others.  \n2. Likes to act with others and make things happen, including in learning.  \n3. Aware of future developments and actively participates.  \n4. Excellent at interpersonal skills and practical knowledge, highly adaptable to others and environments.  \n5. A lover of life, people, and material comforts.'
    },
    'ENFP': {
        'short_desc': 'Extraversion / Intuition / Feeling / Perceiving',
        'features': '1. Enthusiastic, energetic, intelligent, imaginative, sees life full of opportunities but seeks affirmation and support from others.  \n2. Capable of achieving almost anything of interest.  \n3. Quickly finds solutions to problems and offers help to those in need.  \n4. Relies on improvisation rather than planning.  \n5. Often finds reasons to push themselves to achieve goals.  \n6. Spontaneous performers.'
    },
    'ENTP': {
        'short_desc': 'Extraversion / Intuition / Thinking / Perceiving',
        'features': '1. Quick-witted, intelligent, versatile.  \n2. Motivates partners, quick and outspoken.  \n3. Enjoys debating both sides of issues for fun.  \n4. Strategic in solving new and challenging problems, but may overlook or get bored with routine tasks and details.  \n5. Diverse interests, easily shifts to new ones.'
    }
}


if 'llms_mbti' not in st.session_state:
    st.session_state['llms_mbti'] = json.load(
        open('llms_mbti.json', 'r', encoding='utf8')
    )

    models, mbti, shor_desc = [], [], []
    for llm, details in st.session_state['llms_mbti'].items():
        models.append(llm)
        mbti.append(details['res'])
        shor_desc.append(MBTI_DESCRIPTIONS[details['res']]['short_desc'])

    overview_dict = {
        'Model Names': models,
        'Test result': mbti,
        'Brief description of personality': shor_desc
    }
    st.session_state['llms_overview_df'] = pd.DataFrame.from_dict(
        overview_dict
    )

    mbti_questions_dict = json.load(open('mbti_questions.json', 'r', encoding='utf8'))
    
    questions = []
    answersA = []
    answersB = []
    
    for ele in mbti_questions_dict.values():
        row = ele['question'].split('\\n')
        questions.append(row[0])
        answersA.append(row[1])
        answersB.append(row[2])
    
    convert_dict = {
        'MBTITest(93 questions)': questions, # [ele['question'] for ele in mbti_questions_dict.values()]
        'Answers A': answersA,
        'Answers B': answersB,
    }
    st.session_state['mbti_question_df'] = pd.DataFrame.from_dict(convert_dict)


st.dataframe(
    st.session_state['llms_overview_df'], 
    use_container_width=True
)


with st.expander('📚 MBTI Intro', expanded=True):
    st.markdown(":blue[The MBTI analyzes personality on 4 dimensions, each containing 2 opposing preferences.]")
    st.code("""
1. Extraversion E-Introversion I: representing the different sources of energy in each person.
2. Sensing S - Intuition N: representing different brain preferences for sensing.
3. Thinking T - Feeling F: Representing different brain preferences for judgment.
4. judgment J - perception P: whether perception or judgment plays a dominant role in people's adaptation to the external environment.
    """) 
    st.markdown(":blue[Specifically, the following 16 personalities exist:]")
        
    st.code("""
        * ISTJ (Inspector type): Quiet, serious, success through thoroughness and reliability. Practical and responsible. Decisions are logical and move step by step towards the goal, not easily distracted. Likes to keep work, family and life organized. Values tradition and loyalty.
        * ISFJ (Caregiver Type) : Quiet, friendly, responsible and conscientious. Strongly committed to fulfilling their obligations. Thorough, diligent and precise, loyal and considerate, paying attention and remembering small details about the people they value and caring about their feelings. Strive to make their work and home environments orderly and welcoming.
        * INFJ (Fraternal): Seeks meaning and connection between ideas, relationships, material things, etc. Wants to understand what motivates people and has great insight into people. Responsible and adheres to their values. Has a clear vision of how to best serve the public. Is organized and decisive in the achievement of goals.
        * INTJ (Expert): Innovative and driven in realizing their ideas and achieving their goals. They are able to quickly recognize the patterns in the outside world and form long-term visionary plans. Once a decision is made to do something, planning begins and continues until it is accomplished. Suspicious and independent, with high expectations of their own and others' abilities and performance.
        * ISTP (Adventurer Type): Flexible, patient, a quiet observer until a problem occurs, will act immediately to find a practical solution. Analyzes the principles of how things work and can quickly find the key sticking points from a large amount of information. Interested in causes and effects, approaches problems logically and values efficiency.
        * ISFP (Artist Type): Quiet, friendly, sensitive and kind. Enjoys the present. Likes to have their own space and to be able to work on their own schedule. Very loyal and responsible to their values and to the people they feel are important to them. Dislikes arguments and conflicts. Doesn't impose their ideas and values on others.
        * INFP (Philosopher Type): Idealistic, very loyal to their values and to the people they feel are important to them. Wants the external life to be harmonized with their own internal values. Curious and quick to see the possibilities of things and can be a catalyst for realizing ideas. Seeks to understand others and help them realize their potential. Adaptable, flexible and receptive unless it goes against their values.
        * INTP (Scholarly): Seeks to find rational explanations for anything that interests them. Prefers the theoretical and abstract, keen to think rather than socialize. Quiet, introverted, flexible and adaptable. Has an uncanny ability to focus and solve problems in depth in areas of interest to him or her. Suspicious, sometimes a bit critical, and likes to analyze.
        * ESTP (Challenger Type): Flexible, tolerant, practical, results-oriented. Finds theories and abstract explanations very boring. Likes to take active action to solve problems. Focuses on the present, is natural and unpretentious, and enjoys moments with others. Enjoys material pleasures and fashion. The most effective way to learn new things is through hands-on experience and practice.
        * ESFP (Performer Type): Outgoing, friendly and receptive. Loves life, people and material pleasures. Enjoys working with others to make things work. Common sense and practicality in work and making it seem fun. Flexible, naturally unpretentious and quick to adapt to new anything. The most effective way to learn new things is to try them with others.
        * ENFP (Public Relations Type): Enthusiastic and imaginative. Thinks life has many possibilities. Can quickly relate things to information and then very confidently solve problems based on their own judgment. Always needs to be recognized by others and is always ready to give appreciation and help. Flexible, natural and unpretentious, with a strong ability to improvise and speak fluently.
        * ENTP (Intelligent Multi-Tasker Type): Responsive and wise, with the ability to motivate others, alert and outspoken. Resourceful and strategic in solving new and challenging problems. Good at identifying theoretical possibilities and then analyzing them with a strategic eye. Good at understanding others. Dislikes routine and will rarely do the same thing in the same way, tending to develop new hobbies one after the other.
        * ESTJ (Housekeeper type): Practical and realistic. Decisive and will act as soon as he/she makes up his/her mind. Good at organizing projects and people to get things done and getting results in the most efficient way possible. Attentive to day-to-day details. Has a very clear set of logical standards that are systematically followed and expects others to do the same. Strong and forceful in implementing programs.
        * ESFJ (Host Type): Enthusiastic, responsible and cooperative. Wants the surroundings to be cozy and harmonious and carries out decisively to that end. Enjoys working with others to accomplish tasks precisely and in a timely manner. Remains faithful in all matters. Is sensitive to the needs of others in their daily lives and makes every effort to help. Wants to be recognized and appreciated for himself and his actions.
        * ENFJ (Instructive): Enthusiastic, considerate, sensitive and responsible. Very attentive to the feelings, needs and motivations of others. Good at recognizing the potential of others and wants to help them realize it. Can be a catalyst for personal or group growth and progress. Loyal and responds positively to both praise and criticism. Friendly and well socialized. Helps others well in groups and has leadership skills that inspire others.
        * ENTJ (Commander-in-Chief): Honest, decisive and has natural leadership skills. Quick to see irrationality and inefficiency in company/organization procedures and policies, develops and implements effective and comprehensive systems to solve problems. Good at long-term planning and goal setting. Typically well-informed and well-read, enjoys broadening their knowledge and sharing this with others. Very strong and forceful in presenting their ideas.
    """
    )


with st.expander('🧠 LLMs Personality Details', expanded=True):
    
    c1, c2 = st.columns([12, 4])

    with c1:
        select_model = st.selectbox(
            'Select model to view details',
            st.session_state['llms_mbti'].keys()
        )

    with c2:
        model_mbti = st.session_state['llms_mbti'][select_model]['res']
        st.metric(
            'model personality',
            model_mbti,
        )
    
    st.markdown('---')
    st.markdown(MBTI_DESCRIPTIONS[model_mbti]['features'])
    st.markdown('---')

    groups = [
        ('E', 'I'),
        ('S', 'N'),
        ('T', 'F'),
        ('J', 'P'),
    ]

    for group in groups:
        ele1 = st.session_state['llms_mbti'][select_model]['details'][group[0]]
        ele2 = st.session_state['llms_mbti'][select_model]['details'][group[1]]
        total = ele1 + ele2

        ele1_percentage = ele1 / total
        ele2_percentage = ele2 / total

        total_width = 16
        ele1_width = int(total_width * ele1_percentage)
        ele2_width = total_width - ele1_width

        c1, c2 = st.columns([ele1_width, ele2_width])
        with c1:
            if ele1_width > ele2_width:
                st.success(f'{group[0]} ({ele1},{round(ele1_percentage * 100, 1)} %)')
            else:
                st.error(f'{group[0]} ({ele1},{round(ele1_percentage * 100, 1)} %)')
        with c2:
            if ele1_width <= ele2_width:
                st.success(f'{group[1]} ({ele2},{round(ele2_percentage * 100, 1)} %)')
            else:
                st.error(f'{group[1]} ({ele2},{round(ele2_percentage * 100, 1)} %)')


st.dataframe(
    st.session_state['mbti_question_df'],
    use_container_width=True,
    height=800
)

