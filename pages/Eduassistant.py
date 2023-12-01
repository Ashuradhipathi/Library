import streamlit as st
import os
from llama_index import Document, SummaryIndex, LLMPredictor, ServiceContext, load_index_from_storage, VectorStoreIndex
from llama_index.llms import OpenAI
import openai
from constants import *



def generate_questions(questions_str):
    questions = questions_str.split('\n\n')
    return [question.strip() for question in questions if question]

def display_question(question):
    lines = question.split("\n")
    question_text = lines[0]
    st.write(question_text)

def get_llm(llm_name, model_temperature, api_key, max_tokens=256):
    openai.api_key = api_key
    return OpenAI(temperature=model_temperature, model=llm_name, max_tokens=max_tokens)

def init_index(documents, llm_name, model_temperature, api_key):
    llm = get_llm(llm_name, model_temperature, api_key, max_tokens=1024)
    service_context = ServiceContext.from_defaults(llm=llm,
                                                   chunk_size=1024)
    temp_index = SummaryIndex.from_documents(documents, service_context=service_context)
    return temp_index

def extract_terms(documents, term_extract_str, llm_name, model_temperature, api_key):
    st.session_state['temp_index'] = init_index(documents, llm_name, model_temperature, api_key)
    query_engine = st.session_state['temp_index'].as_query_engine(response_mode="tree_summarize")


    terms_definitions = str(query_engine.query(term_extract_str))
    terms_definitions = [x for x in terms_definitions.split("\n") if x and 'Term:' in x and 'Definition:' in x]
    terms_to_definition = {x.split("Definition:")[0].split("Term:")[-1].strip(): x.split("Definition:")[-1].strip() for x in terms_definitions}
    return terms_to_definition

def insert_terms(terms_to_definition):
    new_docs = []
    for term, definition in terms_to_definition.items():
        text = f"Term: {term}\nDefinition: {definition}"
        doc = Document(text=text, doc_id=f"doc_term_{term}")
        new_docs.append(doc)
    st.session_state['llama_index'].insert_nodes(new_docs)
    st.session_state['llama_index'].storage_context.persist('./storage')


@st.cache_resource
def initialize_index(llm_name, model_temperature, api_key):
    """Create the VectorStoreIndex object."""
    llm = get_llm(llm_name, model_temperature, api_key)

    service_context = ServiceContext.from_defaults(llm_predictor=LLMPredictor(llm=llm))

    index = VectorStoreIndex([], service_context=service_context)

    return index

def main():
    st.title("EDU ASSISTANT")


    if "all_terms" not in st.session_state:
        st.session_state["all_terms"] = DEFAULT_TERMS




    setup_tab, terms_tab, upload_tab, query_tab, summary_tab, mcq_tab  = st.tabs(
        ["Setup", "All Terms", "Upload/Extract Terms", "Query Terms", "Outline And Summary", "Practice"]
    )

    with terms_tab:
        st.subheader("Current Extracted Terms and Definitions")
        st.json(st.session_state["all_terms"])

    with setup_tab:
        st.subheader("LLM Setup")
        api_key = st.text_input("Enter your OpenAI API key here", type="password")
        llm_name = st.selectbox('Which LLM?', ["text-davinci-003", "gpt-3.5-turbo", "gpt-4"])
        model_temperature = st.slider("LLM Temperature", min_value=0.0, max_value=1.0, step=0.1)
        term_extract_str = st.text_area("The query to extract terms and definitions with.", value=DEFAULT_TERM_STR)


    with query_tab:
        st.subheader("Query for Terms/Definitions!")
        st.markdown(
            (
                "The LLM will attempt to answer your query, and augment it's answers using the terms/definitions you've inserted. "
                "If a term is not in the index, it will answer using it's internal knowledge."
            )
        )
        if st.button("Initialize Index and Reset Terms", key="init_index_2"):
            st.session_state["llama_index"] = initialize_index(
                llm_name, model_temperature, api_key
            )
            st.session_state["all_terms"] = {}

        if "llama_index" in st.session_state:
            query_text = st.text_input("Ask about a term or definition:")
            if query_text:
                query_text = query_text + "\nIf you can't find the answer, answer the query with the best of your knowledge."
                with st.spinner("Generating answer..."):
                    query_engine = st.session_state["llama_index"].as_query_engine(response_mode="compact")
                    response = str(query_engine.query(query_text))
                st.markdown(str(response))

    with upload_tab:
        st.subheader("Extract and Query Definitions")
        if st.button("Initialize Index and Reset Terms"):
            st.session_state['llama_index'] = initialize_index(llm_name, model_temperature, api_key)
            st.session_state['all_terms'] = {}

        if "llama_index" in st.session_state:
            st.markdown("Enter the text manually.")
            document_text = st.text_area("enter raw text")
            if st.button("Extract Terms and Definitions") and ( document_text):
                st.session_state['terms'] = {}
                terms_docs = {}
                with st.spinner("Extracting..."):
                    terms_docs.update(extract_terms([Document(text=document_text)], term_extract_str, llm_name, model_temperature, api_key))
                st.session_state['terms'].update(terms_docs)

            if "terms" in st.session_state and st.session_state["terms"]:
                st.markdown("Extracted terms")
                st.json(st.session_state['terms'])

                if st.button("Insert terms?"):
                    with st.spinner("Inserting terms"):
                        insert_terms(st.session_state['terms'])
                    st.session_state['all_terms'].update(st.session_state['terms'])
                    st.session_state['terms'] = {}
                    st.rerun()



    with summary_tab:
        st.markdown("Enter the text manually.")
        document_text_ = st.text_area("enter the raw text")
        documents=[Document(text=document_text_)]
        if st.button("Generate Summary") and ( document_text):
            st.session_state['temp_index'] = init_index(documents, llm_name, model_temperature, api_key)
            query_engine = st.session_state['temp_index'].as_query_engine(response_mode="tree_summarize")
            st.markdown("## Outline")
            outline = str(query_engine.query(DEFAULT_OUTLINE_STR))
            st.markdown(outline)
            st.markdown("## Summary")
            response = str(query_engine.query(DEFAULT_SUMMARY_STR))
            st.markdown(response)
            
    with mcq_tab:
        check = False
        if st.button("Generate"):
            if st.session_state['temp_index']:
                check=True
        if check:
            query_engine = st.session_state['temp_index'].as_query_engine(response_mode="tree_summarize")
            mcq = str(query_engine.query(DEFAULT_MCQ_STR))
            questions_list = generate_questions(mcq)

            user_answers = {}
            score = 0
            correct_answers = []

            for i, question in enumerate(questions_list, start=1):
                display_question(question)
            
                options_start = question.find('a.')
                options_end = question.find('Answer:')
                options_str = question[options_start:options_end].strip()
                options = [opt.strip() for opt in options_str.split('\n')]


                user_answer = st.radio(f"Select your answer for {question[:2]}:", options, key=i)
                user_answers[f"{question[:2]}"] = user_answer

                correct_answer_start = question.find("Answer:") + len("Answer:")
                correct_answer = question[correct_answer_start:].strip()
                correct_answers.append(correct_answer)
                if user_answer == correct_answer:
                    score += 1

            st.write(f"\nYour score: {score}/{len(questions_list)}")

            st.markdown('## Correct Answers')
            for i, answer in enumerate(correct_answers):
                st.write(f'Q{i+1} : {answer}')

        else:
            st.markdown('## Go Back and generate summary and read it')
            
if __name__ == "__main__":
    main() 


