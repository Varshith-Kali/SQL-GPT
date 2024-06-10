import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyDn2M4Y01MKNVw3TEWV_ldb3o2UPh7bUAo"

genai.configure(api_key = GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def main():
    # Setting the page configuration before any other Streamlit function
    st.set_page_config(page_title="SQL GPT", page_icon=":robot:")
    
    # Corrected HTML syntax
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>SQL Query Generator 🤖...</h1>
            <h3>It allows users to generate SQL queries !!!</h3>
            <p>This is a simple tool that allows you to generate SQL queries based on your prompts.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    text_input = st.text_area("Enter your prompt :")
    submit = st.button("Submit")

    if submit:
        # response = model.generate_content(text_input) 
        # st.write(response.text)

        with st.spinner("Generating SQL Query..."):
            template = """

            Create a SQL query snippet using below prompt :

            ```
                {text_input}
            ``` 
            Just give the SQL query alone as output.
            
            """

            formatted_template = template.format(text_input = text_input)
            response = model.generate_content(formatted_template)
            sql_query = response.text
            sql_query = sql_query.strip().lstrip("```sql").rstrip("```")
            st.code(sql_query, language="sql")

            explanation_template = """

            Explain the SQL query given below :

            ```
                {sql_query}
            ``` 
            Provide a simple explanation about the SQL query provided.
            
            """

            e_template_formatted = explanation_template.format(sql_query = sql_query)
            explanation = model.generate_content(e_template_formatted)
            st.write(explanation.text)

main()
