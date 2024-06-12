import sys  
sys.path.append('backend')
from index_manager import IndexManager
from openai import OpenAI

class TestPromptGeneration:
    def __init__(self):
        self.index_manager = IndexManager()
        self.data_dict_name = "ordini"
        self.index_manager.createOrLoadIndex(self.data_dict_name)
        # Collegamento a un server in esecuzione su localhost
        # Gli LLM possono essere scaricati da LM Studio
        # Le richieste HTTP e le risposte seguono il formato delle API di OpenAI
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        """ 
        Per connettersi dalla wsl al server di LM Studio in esecuzione su Windows, è possibile inserire l'indirizzo IP
        della macchina locale (visibile con il comando ipconfig)
        """
        # self.client = OpenAI(base_url="http://192.168.x.x:1234/v1", api_key="lm-studio")

    # Riscrittura tramite LLM della richiesta dell'utente 
    def rewriteUserRequest(self, user_request):
        completion = self.client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=[
                {"role": "user", "content": "Rewrite this sentence, always in italian: " + user_request + "\nReturn only the rewritten sentence, without anything else."}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    
    # Creazione della query SQL a partire dal prompt
    def getQuerySQL(self, prompt):
        completion = self.client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=[
                {"role": "user", "content": prompt + "\nReturn only the final SQL query, without anything else."}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content

    # Esecuzione del test
    def iterate_prompt_generation(self, user_request):
        print(user_request + "\n")
        prompt = self.index_manager.promptGenerator(self.data_dict_name, user_request, activate_log=False)
        print(self.getQuerySQL(prompt) + "\n")
        # Rimuovo l'ultima riga dal prompt
        lines = prompt.split('\n')
        lines = lines[:-1]
        prompt = '\n'.join(lines)
        for _ in range(5):
            user_request = self.rewriteUserRequest(user_request)
            print(user_request + "\n")
            # Aggiungo al prompt la frase riscritta
            complete_prompt = prompt + f"\nAnswer with the right SQL query for MariaDB: {user_request}"
            print(self.getQuerySQL(complete_prompt) + "\n")

def main():
    prompt_generation = TestPromptGeneration()
    request_list = [
        "Tutte le informazioni riguardanti gli utenti che hanno pagato i loro ordini con PayPal."
    ]
    print("Test di generazione del prompt:\n")
    for request in request_list:
        prompt_generation.iterate_prompt_generation(request)  

if __name__ == '__main__':
    main()