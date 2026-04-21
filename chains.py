import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from dotenv import load_dotenv

load_dotenv(override=True)

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
                        model="llama-3.1-8b-instant",
                        temperature=0,
                        max_tokens=None,
                        timeout=None,
                        max_retries=2)
    
    
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template("""
                I will give you scraped text from the job posting. 
                Your job is to extract the job details & requirements in a JSON format containing the following keys: 'role', 'experience', 'skills', and 'description'. 
                Only return valid JSON. No preamble, please.
                Here is the scraped text: {page_data}
                """)    
        
        chain_extract = prompt_extract | self.llm
        response = chain_extract.invoke(input={"page_data" : cleaned_text})
        
        try:
            json_parser = JsonOutputParser()
            response = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("Content too big, unable to parse jobs.")
        
        return response if isinstance(response, list) else [response]


    def write_email(self, job_description, portfolio_urls, sender_name, sender_role, sender_company):
        prompt_email = PromptTemplate.from_template(
                """
                I will give you a role and a task that you have to perform in that specific role.
                Your Role: Your name is {sender_name}, you are an incredible {sender_role} who knows how to get clients. You work for {sender_company}, an IT firm providing tailored solutions to clients.
                Your Job: Write a professional, concise cold email to the client regarding the Job opening they have advertised. Pitch the client with a strong email hook offering our services. 
                Add the most relevant portfolio URLs from the list below to showcase our expertise.
                
                IMPORTANT FORMATTING: Ensure the email is formatted professionally. Do not include excessive empty lines or unnecessary spaces between paragraphs. Keep the structure clean and concise.
                
                JOB DESCRIPTION: {job_description}
                ------
                PORTFOLIO URLS: {portfolio_urls}
                """)
        
        chain_email = prompt_email | self.llm
        response = chain_email.invoke({
            "job_description": str(job_description), 
            "portfolio_urls": portfolio_urls,
            "sender_name": sender_name,
            "sender_role": sender_role,
            "sender_company": sender_company
        })

        return response.content
        