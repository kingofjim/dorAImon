from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
)

from dotenv import load_dotenv


class PromptSolutionService:
    def __init__(self):
        load_dotenv()

    def generate_cv_summary_prompt(self, job_title, candidate_resume):
        system_template = """
        I need you to provide me with the candidate's information, which could be a resume or a self-introduction, for the position of {job_title} in an interview.
        Please help me identify the key points in this information, including technical skills (technical keywords), candidate's background (including education), personality interests, achievements (briefly presented), and an overall summary.
        If a specific aspect is not available in the provided information, it can be left out. 
        Please present the analysis in the format of the template provided.
        
        Candidate's resume:
        {candidate_resume}
        """

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            system_template)

        message = system_message_prompt.format(
            job_title=job_title,
            candidate_resume=candidate_resume
        )

        return message

    def generate_job_fit_analysis_prompt(self, job_description, cv_summary):
        system_template = """
        If you are the hiring manager, this is the JD you wrote:
        {job_description}
        
        This is Candidate's CV:
        {cv_summary}
        
        Below is the template for the match analysis, please be brief:
        Job Fit Assessment: 
        """

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            system_template)

        message = system_message_prompt.format(
            job_description=job_description,
            cv_summary=cv_summary
        )

        return message

    def generate_further_question_prompt(self, conversations):
        system_template = """
        You are an assistant tool for interviewing software engineers. You need to help the interviewer with questions based on the subsequent interview dialogue content. The content needs to cover:

        1. More in-depth questions
        2. Extendable questions
        For each point, provide up to three questions and keep them brief so the interviewer can use them directly without needing additional explanations.
        
        {conversations}
        """

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            system_template)

        message = system_message_prompt.format(
            conversations=conversations
        )

        return message

    def generate_interview_analytics(self, job_title, cv_summary, conversations):
        system_template = """
        Assuming you are the interviewing manager, this is the candidate's background:      
        {cv_summary}
            
        This is the dialogue from the interview process:   
        {conversations}

        Please present the following template as follows:  
            
        Applied position:       
        {job_title}
            
        Backgorund:      
        Name:      
        years of experience:      
        Education:      
        Phone:      
            
        Keywords:      
        •      
        •      
        •      
            
        Analysis:      
        1. Knowlege(<score> point): <reason>      
        2. Motive(<score> point): <reason>      
        3. Skill(<score> point): <reason>      
        4. Collaboration(<score> point: <reason>      
        5. Communication(<score> point): <reason>      
            
        Advantage:      
        •      
        •      
        •      
            
        Weakness:      
        •      
        •      
        •      
        
        Summary:
        """

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            system_template)

        message = system_message_prompt.format(
            cv_summary=cv_summary,
            conversations=conversations
        )

        return message

    def generate_interview_job_fit_analysis(self, interview_report, job_description):
        system_template = """
        This is the candidate's interview analysis report:
        {interview_report}
        
        Assuming you are the hiring manager, please provide a candidate-JD alignment analysis based on the following JD and in conjunction with this candidate's analysis report. Identify the points of alignment and non-alignment, and explain the reasons behind them.  

        This is JD: 
        {job_description}
        """

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            system_template)

        message = system_message_prompt.format(
            interview_report=interview_report,
            job_description=job_description
        )

        return message
