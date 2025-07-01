import streamlit as st
import requests
import random

# -------------------
# PAGE CONFIGURATION
# -------------------
st.set_page_config(page_title="TriviaVerse - Wiki Quiz", page_icon="📚", layout="centered")
st.title("📚 TriviaVerse: Wiki-powered Quiz App")
st.markdown("Test your knowledge with real facts from Wikipedia and Wikidata!")

# -------------------
# QUIZ DATA
# -------------------
sample_topics = {
    "Python (Programming Language)": [
        {
            "topic": "Python_(programming_language)",
            "qid": "Q28865",
            "question": "Which of the following is a correct fact about Python?",
            "options": [
                "It was developed by Elon Musk",
                "It is a snake species",
                "It is a high-level programming language",
                "It was released in 2020"
            ],
            "answer": "It is a high-level programming language"
        },
        {
            "topic": "Python_(programming_language)",
            "qid": "Q28865",
            "question": "Who created Python?",
            "options": ["Guido van Rossum", "Elon Musk", "Bill Gates", "Dennis Ritchie"],
            "answer": "Guido van Rossum"
        },
        {
            "topic": "Python_(programming_language)",
            "qid": "Q28865",
            "question": "Python is which type of programming language?",
            "options": ["Compiled", "Low-Level", "High-Level", "Assembly"],
            "answer": "High-Level"
        },
        {
            "topic": "Python_(programming_language)",
            "qid": "Q28865",
            "question": "Which year was Python first released?",
            "options": ["1991", "2000", "1989", "2010"],
            "answer": "1991"
        },
        {
            "topic": "Python_(programming_language)",
            "qid": "Q28865",
            "question": "What is the extension for Python files?",
            "options": [".py", ".java", ".cpp", ".txt"],
            "answer": ".py"
        }
    ],
    "Java": [
        {
            "topic": "Java_(programming_language)",
            "qid": "Q251",
            "question": "Java was originally developed by?",
            "options": ["Sun Microsystems", "Microsoft", "Apple", "IBM"],
            "answer": "Sun Microsystems"
        },
        {
            "topic": "Java_(programming_language)",
            "qid": "Q251",
            "question": "Which year was Java released?",
            "options": ["1995", "2005", "2010", "1985"],
            "answer": "1995"
        },
        {
            "topic": "Java_(programming_language)",
            "qid": "Q251",
            "question": "Java files typically have which extension?",
            "options": [".java", ".js", ".py", ".cpp"],
            "answer": ".java"
        },
        {
            "topic": "Java_(programming_language)",
            "qid": "Q251",
            "question": "Java runs on a virtual machine called?",
            "options": ["JVM", "CLR", "V8", "GVM"],
            "answer": "JVM"
        },
        {
            "topic": "Java_(programming_language)",
            "qid": "Q251",
            "question": "Java's slogan is?",
            "options": ["Write once, run anywhere", "Code for life", "Fast and safe", "High-level for all"],
            "answer": "Write once, run anywhere"
        }
    ],
    "C++": [
        {
            "topic": "C%2B%2B",
            "qid": "Q2407",
            "question": "C++ was developed by?",
            "options": ["Bjarne Stroustrup", "Guido van Rossum", "James Gosling", "Linus Torvalds"],
            "answer": "Bjarne Stroustrup"
        },
        {
            "topic": "C%2B%2B",
            "qid": "Q2407",
            "question": "C++ was created as an extension of which language?",
            "options": ["C", "Java", "Python", "Assembly"],
            "answer": "C"
        },
        {
            "topic": "C%2B%2B",
            "qid": "Q2407",
            "question": "Which year was C++ first released?",
            "options": ["1985", "1995", "2005", "1970"],
            "answer": "1985"
        },
        {
            "topic": "C%2B%2B",
            "qid": "Q2407",
            "question": "What is the file extension for C++ source files?",
            "options": [".cpp", ".c", ".java", ".py"],
            "answer": ".cpp"
        },
        {
            "topic": "C%2B%2B",
            "qid": "Q2407",
            "question": "C++ supports which programming paradigm?",
            "options": ["Object-oriented", "Functional only", "Logic only", "None"],
            "answer": "Object-oriented"
        }
    ],
    "C": [
        {
            "topic": "C_(programming_language)",
            "qid": "Q1575",
            "question": "Who developed the C programming language?",
            "options": ["James Gosling", "Dennis Ritchie", "Guido van Rossum", "Bjarne Stroustrup"],
            "answer": "Dennis Ritchie"
        },
        {
            "topic": "C_(programming_language)",
            "qid": "Q1575",
            "question": "C was initially developed at which organization?",
            "options": ["Microsoft", "Bell Labs", "Apple", "Sun Microsystems"],
            "answer": "Bell Labs"
        },
        {
            "topic": "C_(programming_language)",
            "qid": "Q1575",
            "question": "Which year was the C language first released?",
            "options": ["2002", "1972", "1982", "1992"],
            "answer": "1972"
        },
        {
            "topic": "C_(programming_language)",
            "qid": "Q1575",
            "question": "C is known as a ____ language?",
            "options": ["Machine-level", "High-level", "Assembly-level", "Low-level"],
            "answer": "High-level"
        },
        {
            "topic": "C_(programming_language)",
            "qid": "Q1575",
            "question": "Which of these file extensions is commonly used for C?",
            "options": [".cpp", ".java", ".c", ".py"],
            "answer": ".c"
        }
    ]
}

# -------------------
# SESSION STATE INIT
# -------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = None
if "question_indices" not in st.session_state:
    st.session_state.question_indices = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False
if "shuffled_options" not in st.session_state:
    st.session_state.shuffled_options = {}

# -------------------
# WIKI FETCH FUNCTIONS
# -------------------
def fetch_wikipedia_summary(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No summary available."), data.get("title", topic)
    return "No data found.", topic

def fetch_wikidata_fact(qid):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            entity = data['entities'][qid]
            label = entity['labels']['en']['value']
            description = entity['descriptions']['en']['value']
            return label, description
        except:
            return "No fact found.", ""
    return "No fact found.", ""

# -------------------
# QUIZ MODE
# -------------------
def show_quiz():
    if not st.session_state.quiz_started:
        topic_key = st.selectbox("Choose a topic:", list(sample_topics.keys()))
        if st.button("Start Quiz"):
            st.session_state.quiz_topic = topic_key
            st.session_state.quiz_started = True
            st.session_state.score = 0
            st.session_state.total = 0
            st.session_state.current_question = 0
            st.session_state.question_indices = list(range(len(sample_topics[topic_key])))
            st.session_state.answer_submitted = False
            st.session_state.shuffled_options = {}
        return

    if st.session_state.current_question >= len(st.session_state.question_indices):
        st.success(f"🎉 Quiz Completed! Your final score: {st.session_state.score}/{len(sample_topics[st.session_state.quiz_topic])}")
        if st.button("Restart Quiz"):
            st.session_state.quiz_started = False
            st.session_state.answer_submitted = False
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.total = 0
        return

    topic_questions = sample_topics[st.session_state.quiz_topic]
    q_index = st.session_state.question_indices[st.session_state.current_question]
    q = topic_questions[q_index]

    # shuffle options once per question
    if q_index not in st.session_state.shuffled_options:
        opts = q["options"].copy()
        random.shuffle(opts)
        st.session_state.shuffled_options[q_index] = opts

    options = st.session_state.shuffled_options[q_index]

    st.subheader(f"Question {st.session_state.current_question + 1}: {q['question']}")
    choice = st.radio("Select your answer:", options, key=f"choice_{st.session_state.current_question}")

    if not st.session_state.answer_submitted:
        if st.button("Submit Answer"):
            st.session_state.total += 1
            st.session_state.answer_submitted = True
            if choice == q["answer"]:
                st.session_state.score += 1
                st.success("✅ Correct Answer!")
            else:
                st.error(f"❌ Wrong! Correct answer: {q['answer']}")

            summary, title = fetch_wikipedia_summary(q["topic"])
            st.markdown(f"**📘 Wikipedia Summary for {title}:**")
            st.info(summary)

            label, description = fetch_wikidata_fact(q["qid"])
            st.markdown(f"**📊 Wikidata Fact about {label}:**")
            st.success(description)
    else:
        if st.button("Next Question"):
            st.session_state.answer_submitted = False
            st.session_state.current_question += 1
            st.rerun()

# -------------------
# FLASHCARD MODE
# -------------------
def flashcard_mode():
    st.subheader("🧠 Flashcard Learning Mode")

    topics = [
        "Python_(programming_language)",
        "Java_(programming_language)",
        "C%2B%2B",
        "C_(programming_language)",
        "Artificial_intelligence",
        "Machine_learning",
        "Computer_science",
        "Algorithm",
        "Blockchain",
        "Cybersecurity",
        "Data_structure"
    ]

    if "current_flashcard" not in st.session_state:
        st.session_state.current_flashcard = random.choice(topics)

    def get_flashcard_content(topic):
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("title", topic), data.get("extract", "No summary available.")
        return topic, "No data found."

    title, summary = get_flashcard_content(st.session_state.current_flashcard)
    
    st.markdown(f"### 📘 {title}")
    st.info(summary)

    if st.button("Next Card 🔁"):
        st.session_state.current_flashcard = random.choice(topics)
        st.rerun()

# -------------------
# SIDEBAR NAVIGATION
# -------------------
st.sidebar.title("📌 Menu")
page = st.sidebar.radio("Go to", ["Quiz Mode", "Flashcard Mode", "Scoreboard"])

if page == "Quiz Mode":
    show_quiz()
elif page == "Flashcard Mode":
    flashcard_mode()
else:
    st.header("📊 Scoreboard")
    st.metric("Questions Answered", st.session_state.total)
    st.metric("Correct Answers", st.session_state.score)
    if st.button("🔄 Reset Score"):
        st.session_state.score = 0
        st.session_state.total = 0
        st.success("Scoreboard has been reset.")
