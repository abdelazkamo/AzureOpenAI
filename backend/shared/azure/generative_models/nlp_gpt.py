from openai import AzureOpenAI


from .message_builder import MessageBuilder



class NlpModel:
    def __init__(self, app_config):
        self.app_config = app_config

    def config(
        self,
        user_query: str,
        system_prompt: str,
        model_name: str,
    ):
       
        self.deployment_model_name = self.app_config["AZURE_GPT_DEPLOYMENT_NAME"]
        azure_openai_base_url = f"{self.app_config["AZURE_GPT_API_KEY"]}/openai/deployments/{self.deployment_model_name}/chat/completions?api-version={self.app_config["AZURE_GPT_API_VERSION"]}"
        self.openai_client = AzureOpenAI(
            api_version=self.app_config["AZURE_GPT_API_VERSION"],
            api_key=self.app_config["AZURE_GPT_API_KEY"],
            base_url=azure_openai_base_url,
        )
        self.message_builder = MessageBuilder(system_prompt, model_name)
        self.message_builder.insert_message("user", user_query)

    def run(self, should_structure: bool = True,stream: bool = False):
        chat_completion = self.openai_client.chat.completions.create(
            model=self.deployment_model_name,
            messages=self.message_builder.messages,
            temperature=0.1,
            max_tokens=10000,
            n=1,
            response_format={"type": "json_object"} if should_structure else None,
            stream=stream,
        )
        return chat_completion

    
