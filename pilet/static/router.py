from llama_index.core import PromptTemplate

input_prompt = PromptTemplate(
    "Some choices are given below. It is provided in a numbered list (1 to"
    " {num_choices}), where each item in the list corresponds to a"
    " summary.\n---------------------\n{context_list}\n---------------------\nUsing"
    " only the choices above and not prior knowledge, return the top choices"
    " (no more than {max_outputs}, but only select what is needed) that are"
    " most relevant to the question: '{query_str}'\n"
)
