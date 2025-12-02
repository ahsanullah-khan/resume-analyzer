
from step3a_imports import AnalysisState, SystemMessage, HumanMessage
from step3b_models import llm
from step3c_utils import clean_suggestions

def generate_suggestions_node(state: AnalysisState) -> AnalysisState:
    """Generate AI-powered improvement suggestions"""
    resume_text = state["resume_text"][:1000]
    job_desc = state["job_description"][:1000]
    missing_skills = state["keyword_matches"]["missing_skills"]
    match_percentage = state["match_percentage"]
    resume_years = state["keyword_matches"]["resume_years"]
    job_years = state["keyword_matches"]["job_years"]

    prompt = f"""
    Analyze this resume against the job description and provide SPECIFIC improvement suggestions.

    RESUME EXCERPT: {resume_text}
    JOB DESCRIPTION EXCERPT: {job_desc}

    CURRENT ANALYSIS:
    - Match Score: {match_percentage}%
    - Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}
    - Resume Experience: {resume_years} years | Job Required: {job_years} years

    Provide 3-5 CONCRETE, ACTIONABLE suggestions focusing on skills, experience gaps, and keywords.
    Return ONLY numbered suggestions.
    """

    messages = [
        SystemMessage(content="You are a professional resume coach. Provide direct, specific advice."),
        HumanMessage(content=prompt)
    ]

    try:
        response = llm.invoke(messages)
        suggestions = clean_suggestions(response.content)
    except Exception:
        suggestions = [
            "Add more specific achievements and metrics",
            "Include relevant certifications or training",
            "Highlight leadership experience and team management skills"
        ]

    return {
        "suggested_changes": suggestions,
        "missing_skills": missing_skills
    }
