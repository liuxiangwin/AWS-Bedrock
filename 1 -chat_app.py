import streamlit as st  # Importing Streamlit for building the web interface

from aws_bedrock import initialize_bedrock_client, invoke_bedrock_model  # Importing functions from aws_bedrock.py

# Initialize the AWS Bedrock client using the provided function
client = initialize_bedrock_client()

# Set the title for the app
st.title("Chatbot Powered by AWS Bedrock")

# Add a description or instructions for users
st.markdown("Interact with the AI model hosted on AWS Bedrock using Anthropic Claude!")

# Input field for the user to type a message
user_input = st.text_input(
    "You:",  # Label for the input field
    placeholder="Type your message here...",  # Placeholder text
    key="user_input"  # Unique key for maintaining state
)

# Use Streamlit's session state to store chat history
# This ensures the conversation persists across interactions
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize chat history if not present

# Add a button for the user to submit their message
if st.button("Send"):  # Check if the 'Send' button is clicked
    if user_input.strip():  # Ensure the input is not empty or just whitespace
        with st.spinner("Thinking..."):  # Show a spinner while processing the response
            try:
                # Call the invoke_bedrock_model function to get the chatbot's response
                bot_response = invoke_bedrock_model(client, user_input)
                
                # Append the user's input and chatbot's response to the chat history
                st.session_state.chat_history.append(("You", user_input))  # User's message
                st.session_state.chat_history.append(("Chatbot", bot_response))  # Chatbot's response
            except Exception as e:
                # Display an error message if something goes wrong
                st.error(f"An error occurred: {e}")

# Display the chat history in a conversational format
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")  # Format the chat messages with bold sender names

# Add a button to clear the chat history (optional feature)
if st.button("Clear Chat"):  # Check if the 'Clear Chat' button is clicked
    st.session_state.chat_history = []  # Reset the chat history




    