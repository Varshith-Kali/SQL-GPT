import streamlit as st
import pandas as pd
import sqlite3
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

    query_type = st.selectbox("Select Query Type", ["SQL", "MongoDB"])

    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)

        st.write("Uploaded Database:")
        st.write(df.head())

        # Generate the structure of the database
        table_structure = "\n".join([f"{col}: {dtype}" for col, dtype in zip(df.columns, df.dtypes)])
    else:
        table_structure = None


    text_input = st.text_area("Enter your prompt:")
    submit = st.button("Submit")

    if submit:
        with st.spinner("Generating Query..."):
            if query_type == "SQL":
                if table_structure:
                    template = f"""
                    Given the table structure below, create a SQL query snippet using the following prompt:
                    
                    Table structure:
                    {table_structure}
                    
                    Prompt:
                    ```
                    {text_input}
                    ``` 
                    Just give the SQL query alone as output.
                    """
                else:
                    template = f"""
                    Create a SQL query snippet using the following prompt:
                    
                    Prompt:
                    ```
                    {text_input}
                    ``` 
                    Just give the SQL query alone as output.
                    """
            else:
                if table_structure:
                    template = f"""
                    Given the table structure below, create a MongoDB query snippet using the following prompt:
                    
                    Table structure:
                    {table_structure}
                    
                    Prompt:
                    ```
                    {text_input}
                    ``` 
                    Just give the MongoDB query alone as output.
                    """
                else:
                    template = f"""
                    Create a MongoDB query snippet using the following prompt:
                    
                    Prompt:
                    ```
                    {text_input}
                    ``` 
                    Just give the MongoDB query alone as output.
                    """

            response = model.generate_content(template)
            query = response.text.strip().strip("```sql").strip("```mongodb").strip()

            if query_type == "SQL":
                st.code(query, language="sql")

                if uploaded_file:
                    # Execute SQL query on the DataFrame
                    conn = sqlite3.connect(':memory:')
                    df.to_sql('uploaded_table', conn, index=False, if_exists='replace')

                    try:
                        # Replace table_name with the actual table name used in the database
                        query = query.replace("table_name", "uploaded_table")

                        # Ensure single quotes are properly handled in the query
                        query = query.replace('"', "'")

                        query_result = pd.read_sql_query(query, conn)
                        st.write("Query Result:")
                        st.write(query_result)
                    except Exception as e:
                        st.error(f"Error executing query: {e}")
                    finally:
                        conn.close()
                
            else:
                st.code(query, language="json")

            explanation_template = f"""
            Explain the {query_type} query given below:
            ```
            {query}
            ``` 
            Provide a simple explanation about the {query_type} query provided.
            """

            explanation = model.generate_content(explanation_template)
            st.write(explanation.text)

main()
