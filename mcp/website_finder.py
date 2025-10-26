import os
import google.generativeai as genai
from typing import List, Dict


class WebsiteFinder:
    def __init__(self, api_key: str = None, num_websites: int = 3):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.num_websites = num_websites
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def find_websites_for_part(self, part_name: str) -> List[str]:
        # use gemini to find relevant supplier websites for a specific part
        prompt = f"""Find {self.num_websites} reputable websites where I can purchase the following electronic/mechanical part: {part_name}
        
        Return ONLY a list of website URLs, one per line, without any additional text or explanation.
        Focus on well-known suppliers like Digikey, Mouser, Newark, Arrow, Adafruit, SparkFun, McMaster-Carr, etc.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # parse the response to extract urls
            websites = []
            for line in response.text.strip().split('\n'):
                line = line.strip()
                if line and ('http://' in line or 'https://' in line or line.startswith('www.')):
                    # clean up the url
                    if not line.startswith('http'):
                        line = 'https://' + line
                    websites.append(line)
            
            return websites[:self.num_websites]
        except Exception as e:
            print(f"error finding websites for {part_name}: {e}")
            return ["https://www.adafruit.com/"] # fallback to adafruit
    
    def find_websites_for_parts(self, parts: List[str]) -> Dict[str, List[str]]:
        # find relevant websites for all parts in the bom
        results = {}
        for part in parts:
            print(f"finding websites for: {part}")
            results[part] = self.find_websites_for_part(part)
        return results


