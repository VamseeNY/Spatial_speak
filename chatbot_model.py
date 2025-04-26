from demo_notebook import analyze_agricultural_trends

def get_response(user_query):
    """Get response from the trained Ollama model."""
    try:
        response = analyze_agricultural_trends(user_query)
        return response
    except Exception as e:
        return f"Error generating response: {str(e)}"
