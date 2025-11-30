import streamlit as st
import time
from backend import run_graph, interactive_run

st.title("🔄 Interactive Query Processing Dashboard")

# Initialize state
if "latest_response" not in st.session_state:
    st.session_state.latest_response = None

if "final_output" not in st.session_state:
    st.session_state.final_output = None

# Input bar for user query
query = st.text_input("Enter your query:")

# Submit query
if st.button("Submit Query"):
    if query.strip() == "":
        st.warning("Please enter a query.")
    else:
        st.session_state.latest_response = run_graph(query)
        st.session_state.final_output = None

# Display backend response (if exists)
if st.session_state.latest_response:
    st.subheader("Backend Response:")
    st.write(st.session_state.latest_response)

    st.write("Do you approve this result?")
    col1, col2 = st.columns(2)

    # User approves
    if col1.button("👍 Approve"):
        st.session_state.latest_response = interactive_run("approved")
        st.session_state.final_output = st.session_state.latest_response
        st.success("Final output approved and submitted to backend.")
        st.session_state.latest_response = None

    # User rejects and wants reprocessing
    if col2.button("🔄 Reprocess"):
        st.session_state.latest_response = interactive_run("No")

# Display final approved result
if st.session_state.final_output:
    st.subheader("✅ Final Approved Output")
    st.write(st.session_state.final_output)
