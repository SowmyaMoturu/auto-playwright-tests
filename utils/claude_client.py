import os
import json
import requests
from typing import Dict, List, Optional, Union

class ClaudeClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

    def predict(self, 
                system_prompt: str,
                user_message: str,
                max_tokens: int = 4096,
                temperature: float = 0.2) -> str:
        """
        Send a prediction request to Claude API
        """
        try:
            data = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            
            return response.json()["content"][0]["text"]
            
        except Exception as e:
            raise Exception(f"Error calling Claude API: {str(e)}")

    def predict_in_chunks(self,
                         system_prompt: str,
                         user_messages: List[str],
                         max_tokens: int = 4096,
                         temperature: float = 0.2) -> List[str]:
        """
        Send multiple prediction requests to Claude API and combine results
        """
        results = []
        for message in user_messages:
            result = self.predict(
                system_prompt=system_prompt,
                user_message=message,
                max_tokens=max_tokens,
                temperature=temperature
            )
            results.append(result)
        return results 