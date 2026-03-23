import streamlit as st
import pandas as pd

# ===== Global CSS to reduce vertical spacing =====
st.markdown("""
    <style>
    /* Reduce gap between vertical elements */
    div[data-testid="stVerticalBlock"] {
        gap: 0.25rem; /* Default is ~1rem */
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.header(':rainbow[Welcome!]')
mytext= ('Chapter List:')
st.sidebar.markdown(f"####  :blue[{mytext}]")

# Find number of chapters and chapter names from file 'Q_Bank.xlsx' and store them only once during the session
if 'chapters_list' not in st.session_state:
    df_full= pd.read_excel('./DATA/Q_Bank.xlsx')
    chapters= df_full['Chapter'].unique().tolist()
    chapters.sort()
    if 'chapter_count' not in st.session_state:
        st.session_state.chapter_count = len(chapters)
    if 'df_full' not in st.session_state:
        st.session_state.df_full = df_full
    if 'chapters' not in st.session_state:
        st.session_state.chapters= chapters
    st.session_state.chapters_list= 'prepared'

st.markdown('### 🦄 :yellow[Sample GCSE MCQ (Year-8 Science)]')

# Display the chapters in sidebar
for i, chap in enumerate(st.session_state.chapters, start= 1):
    st.sidebar.markdown(f'######  {i}. {chap}')

# Display a message in sidebar
mytext = 'This app is under trial. Full version will be released after trial period. Thanks for your attention!'
with st.sidebar.container(border= True):
    st.markdown(f"######  *:yellow[{mytext}]*")

def chap_changed():
    if 'q_prepared' in st.session_state:
        del st.session_state.q_prepared
    if 'questions' in st.session_state:
        del st.session_state.questions
    if 'score' in st.session_state:
        del st.session_state.score
    if 'dis_control' in st.session_state:
        del st.session_state.dis_control
    if 'correct_answer_given' in st.session_state:
        del st.session_state.correct_answer_given
        
# Select a chapter
st.write('---')
st.markdown(f'Select chapter number (1 to {st.session_state.chapter_count}):')
chapter_num = st.number_input(label = 'label',
    min_value = 1,
    max_value = st.session_state.chapter_count,
    value = 1,
    format = '%d',
    label_visibility= 'collapsed',
    on_change= chap_changed
    )
st.write('---')
chapter = st.session_state.chapters[chapter_num-1]

#Prepare questions for the selected chapter
if 'q_prepared' not in st.session_state:
    #df_filtered= st.session_state.df_full[st.sesssion_state.df_full['Chapter']= chapter]
    chap_selected= chapter
    df = st.session_state.df_full
    df_filtered = df[df['Chapter'] == chap_selected]
    # Shuffle in place
    if 'questions' not in st.session_state:
        st.session_state.questions = df_filtered.sample(frac=1, random_state=None).reset_index(drop=True)
        q_total = len(st.session_state.questions)
    st.session_state.q_prepared= 'prepared'
                          
chap_text = f'Chapter-{chapter_num}: {chapter}'
st.markdown(f'####      :blue[{chap_text}]')
st.markdown(f'*:blue[(Total {len(st.session_state.questions)} questions)]*')
st.write('---')

# Initialise score
if 'score' not in st.session_state:
    st.session_state.score= 0

# Create a control variable to control the disable the radio and submit buttons
# This is required to disable these widgets once submitted
if 'dis_control' not in st.session_state:
    st.session_state.dis_control = [False] * len(st.session_state.questions)

# Loop through questions
for i, row in st.session_state.questions.iterrows():
    colX, colY= st.columns([10, 90])
    with colX:
        st.markdown(f"👉Q{i+1}:")
    with colY:
        st.markdown(f"{row['Question']}")
    options = [row['Opt1'], row['Opt2'], row['Opt3'], row['Opt4']]
    match row['Answer']:
        case 1:
            correct_answer = row['Opt1']
        case 2:
            correct_answer = row['Opt2']
        case 3:
            correct_answer = row['Opt3']
        case 4:
            correct_answer = row['Opt4']
    
    col_A, col_B= st.columns([12, 88])
    with col_B:
        choice = st.radio("*Choose your answer:*", options, key=f"q{i}",
                          disabled= st.session_state.dis_control[i])
    
    # Create state variables for correct and incorrect answers
    if 'correct_answer_given' not in st.session_state:
        st.session_state.correct_answer_given= [False] * len(st.session_state.questions)
    col1, col2, col3= st.columns([5, 25, 70])
    with col2:
        butt_clicked= st.button(f"Submit answer", key=f"submit{i}",
                                disabled= st.session_state.dis_control[i])
    if butt_clicked:
        with col3:
            if choice == correct_answer:
                st.markdown("✅ :green[Correct!]")
                st.session_state.correct_answer_given[i]= True
                st.session_state.score += 1
            else:
                st.markdown(f"❌ :red[Wrong!] :green[Correct answer: {correct_answer}]")
                st.session_state.correct_answer_given[i]= False
        st.session_state.dis_control[i]= True
        st.rerun()
    if st.session_state.dis_control[i]:
        with col3:
            if st.session_state.correct_answer_given[i]:
                st.markdown("✅ :green[Correct!]")
            else:
                st.markdown(f"❌ :red[Wrong!] :green[Correct answer: {correct_answer}]")

st.write("---")
st.write(f"###### Your final score👉 {st.session_state.score}/{len(st.session_state.questions)}")