from typing import List, Optional
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class CodeyClient:
    def __init__(self, 
                 project_id: str,
                 location: str = "us-central1",
                 max_output_tokens: int = 1024,
                 temperature: float = 0.2):
        """
        Initialize Codey client using code-bison model
        
        Args:
            project_id: GCP project ID
            location: GCP region
            max_output_tokens: Maximum number of tokens in the response
            temperature: Temperature for response generation
        """
        self.llm = VertexAI(
            model_name="code-bison",
            project=project_id,
            location=location,
            max_output_tokens=max_output_tokens,
            temperature=temperature
        )

    def predict(self, 
                system_prompt: str,
                user_message: str) -> str:
        """
        Send a prediction request to Codey
        """
        try:
            # Create prompt template
            template = f"{system_prompt}\n\n{{user_input}}"
            prompt = PromptTemplate(
                template=template,
                input_variables=["user_input"]
            )
            
            # Create chain
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # Get prediction
            return chain.predict(user_input=user_message)
            
        except Exception as e:
            raise Exception(f"Error calling Codey API: {str(e)}")

    def predict_in_chunks(self,
                         system_prompt: str,
                         user_messages: List[str]) -> List[str]:
        """
        Send multiple prediction requests to Codey and combine results
        """
        results = []
        for message in user_messages:
            result = self.predict(
                system_prompt=system_prompt,
                user_message=message
            )
            results.append(result)
        return results 