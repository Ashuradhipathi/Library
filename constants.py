DEFAULT_TERMS = {
"Cake":"Flour confection made from flour, sugar, and other ingredients and is usually baked.",
"Flour":"A powder made by grinding cereal grains, typically wheat, used to make bread, cakes, and pastry.",
"Sugar":"A sweet crystalline substance obtained from various plants, especially sugar cane and sugar beet, consisting essentially of sucrose, and used as a sweetener in food and drink."}

DEFAULT_OUTLINE_STR = ("Design an outline for the given context as if you were a teacher preparing a lesson. Structure it with clear headings, subheadings, and line breaks for an organized presentation. Ensure that each element, including headings and subheadings, is on a separate line for a neat and elegant layout.")
DEFAULT_SUMMARY_STR = (
    "Create a concise overview of the given context.")
DEFAULT_MCQ_STR = (
    "You are a Teacher/ Professor. Your task is to setup "
    "formulate three question that captures an important fact from the "
    "context. Restrict the question to the context information provided."
    "Also Generate three options for each question, out of which only one is correct"
    "Please do specify the right answer also in the format"
    """Q1. What is the purpose of a rocket? 
    a. To control the flight of rockets 
    b. To accelerate without using the surrounding air 
    c. To generate large accelerations 
    Answer: b. To accelerate without using the surrounding air

    Q2. What is the advantage of rockets compared to airbreathing engines? 
    a. They are lightweight and powerful 
    b. They are capable of generating large accelerations 
    c. They are capable of attaining escape velocity from Earth 
    Answer: a. They are lightweight and powerful"""
    ""
    
)

DEFAULT_TERM_STR = (
    "Make a list of terms and definitions that are defined in the context, "
    "with one pair on each line. "
    "If a term is missing it's definition, use your best judgment. "
    "Write each line as as follows:\nTerm: <term> Definition: <definition>"
)