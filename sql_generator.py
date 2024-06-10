import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyDn2M4Y01MKNVw3TEWV_ldb3o2UPh7bUAo"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def main():
    
    st.set_page_config(page_title="Query Generator", page_icon=":robot:")
    
    
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Query Generator 🤖...</h1>
            <h3>Generate SQL or MongoDB queries based on your prompts!</h3>
            <p>This tool allows you to generate SQL or MongoDB queries based on your input.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("Upload your database file (CSV or Excel)", type=["csv", "xlsx"])

    query_type = st.radio("Select Query Type:", ("SQL", "MongoDB"))

    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        
        st.write("Uploaded Database:")
        st.write(df.head())

        # Generate the structure of the database
        table_structure = "\n".join([f"{col}: {dtype}" for col, dtype in zip(df.columns, df.dtypes)])

        
    text_input = st.text_area("Enter your prompt:")
    submit = st.button("Submit")

    if submit:
        with st.spinner("Generating Query..."):
            if query_type == "SQL":
                template = """
                Create a SQL query snippet using the below prompt:
                ```
                {text_input}
                ``` 
                Just give the SQL query alone as output.
                """
            else:
                template = """
                Create a MongoDB query snippet using the below prompt:
                ```
                {text_input}
                ``` 
                Just give the MongoDB query alone as output.
                """

            formatted_template = template.format(text_input=text_input)
            response = model.generate_content(formatted_template)
            query = response.text.strip().strip("```sql").strip("```mongodb").strip()

            if query_type == "SQL":
                st.code(query, language="sql")
            else:
                st.code(query, language="json")

            explanation_template = """
            Explain the {query_type} query given below:
            ```
            {query}
            ``` 
            Provide a simple explanation about the {query_type} query provided.
            """

            e_template_formatted = explanation_template.format(query=query, query_type=query_type)
            explanation = model.generate_content(e_template_formatted)
            st.write(explanation.text)

main()
