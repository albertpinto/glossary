from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import os

# Define LLM constants
RESEARCHER_LLM = 'gpt-4'
REVIEWER_LLM = 'gpt-4'
OUTPUT_FILE = 'glossary'

# Define the Pydantic models for the glossary
class GlossaryItem(BaseModel):
    term: str = Field(..., title="Term", description="The term to define")
    definition: str = Field(..., title="Definition", description="The definition of the term")
    details: str = Field(..., title="Details", description="Details of the term")
    example: Optional[str] = Field(None, title="Example", description="An example of the term in use")

class Glossary(BaseModel):
    glossary: List[GlossaryItem] = Field(..., title="Glossary", description="A list of terms and definitions")

@CrewBase
class GlossaryCrew():
    """Glossary crew"""

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            llm=RESEARCHER_LLM,
            verbose=True
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer'],
            llm=REVIEWER_LLM,
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            output_json=Glossary,
        )

    @task
    def reviewer_task(self) -> Task:
        return Task(
            config=self.tasks_config['reviewer_task'],
            output_file=OUTPUT_FILE + '.json',
            output_json=Glossary,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Glossary crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def convert_json_to_markdown(self, json_file_path: str, markdown_file_path: str) -> None:
        def process_item(item, level=1):
            md_content = ""
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, (str, int, float)):
                        md_content += f"{'#' * level} {key}\n\n{value}\n\n"
                    elif isinstance(value, list):
                        md_content += f"{'#' * level} {key}\n\n"
                        for list_item in value:
                            md_content += process_item(list_item, level + 1)
                    elif isinstance(value, dict):
                        md_content += f"{'#' * level} {key}\n\n"
                        md_content += process_item(value, level + 1)
                    elif value is None:
                        md_content += f"{'#' * level} {key}\n\n"
            elif isinstance(item, list):
                for list_item in item:
                    md_content += process_item(list_item, level)
            return md_content

        try:
            # Read the JSON file
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
            
            # Convert to Markdown
            markdown_content = process_item(data)
            
            # Write to the Markdown file
            with open(markdown_file_path, 'w') as md_file:
                md_file.write(markdown_content)
            
            print(f"Successfully converted '{json_file_path}' to '{markdown_file_path}'.")
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def run_and_convert(self, inputs: Dict[str, Any]) -> None:
        """Run the crew and convert the output to Markdown"""
        self.crew().kickoff(inputs=inputs)
        self.convert_json_to_markdown(OUTPUT_FILE + ".json", OUTPUT_FILE + ".md")