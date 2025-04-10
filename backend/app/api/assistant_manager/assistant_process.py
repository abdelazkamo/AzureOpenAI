from app.shared.azure.generative_models.nlp_gpt import NlpModel
from app.shared.azure.generative_models.prompt_definer import PromptDefiner


class AssistantProcess:
    def __init__(self, app_config):
        self.app_config = app_config
        self.nlp_model = NlpModel(app_config)

    async def get_data_from_db(self, user_query: str):
        self.nlp_model.config(
            user_query=user_query, system_prompt=PromptDefiner.data_retriever_prompt
        )
        result = self.nlp_model.run(should_structure=True)
        return result

    async def generate_response(self, user_query: str):
        self.nlp_model.config(
            user_query=user_query, system_prompt=PromptDefiner.data_interpreter_prompt
        )
        result = self.nlp_model.run(should_structure=False)
        print(result)
        return result
