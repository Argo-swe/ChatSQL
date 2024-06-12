import sys  
sys.path.append('backend')
from index_manager import IndexManager
from pathlib import Path
from openai import OpenAI

current_dir = Path(__file__).resolve().parent

class TestPromptGeneration:
    def __init__(self):
        """
        Nelle impostazioni del server di LM Studio, è opportuno abilitare il flag GPU Offload.
        Questo per evitare che la CPU debba svolgere tutto il lavoro, diminuendo significativamente le prestazioni.
        Bisogna scegliere quanti model layers scaricare sulla GPU (dipende dal modello e dalla GPU).
        Model layers: 0 se il sistema non dispone di GPU Acceleration.
        Model layers: Low (scelta conservativa).
        Model layers: 10-20 (buona scelta iniziale).
        Model layers: 50/50 (metà dei model layers vengono caricati nella memoria della GPU).
        Model layers: Max (l'intero modello viene caricato nella memoria della GPU).
        """
        self.index_manager = IndexManager()
        self.data_dict_name = "orders"
        self.index_manager.createOrLoadIndex(self.data_dict_name)
        self.log_name = f"{current_dir}/prompt_to_sql_log.txt"
        # Collegamento a un server in esecuzione su localhost
        # Gli LLM possono essere scaricati da LM Studio
        # Le richieste HTTP e le risposte seguono il formato delle API di OpenAI
        #self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        """ 
        Per connettersi dalla wsl al server di LM Studio in esecuzione su Windows, è possibile inserire l'indirizzo IP
        della macchina locale (visibile con il comando ipconfig)
        """
        self.client = OpenAI(base_url="http://192.168.1.110:1234/v1", api_key="lm-studio")

    # Riscrittura tramite LLM della richiesta dell'utente 
    def rewriteUserRequest(self, user_request):
        completion = self.client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=[
                {"role": "user", "content": "Just return this slightly rewritten sentence: " + user_request}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content.splitlines()[-1]
    
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
    def iterate_prompt_generation(self, iteration, user_request):
        if iteration == 0:
            log = open(self.log_name, "w")
        else:
            log = open(self.log_name, "a")
        log.write(f"Test {iteration}:\n")
        log.write("Request: " + user_request + "\n")
        prompt = self.index_manager.promptGenerator(self.data_dict_name, user_request, activate_log=False)
        log.write(self.getQuerySQL(prompt) + "\n\n")
        # Rimuovo le ulime due righe dal prompt
        lines = prompt.split('\n')
        lines = lines[:-2]
        prompt = '\n'.join(lines)
        for i in range(5):
            rewritten_sentence = self.rewriteUserRequest(user_request)
            log.write("Request: " + rewritten_sentence + "\n")
            # Aggiungo al prompt la frase riscritta
            temp = (
                f"\nUser request: {rewritten_sentence}"
                "\nConvert user request to SQL query for MariaDB")
            complete_prompt = prompt + temp
            log.write(self.getQuerySQL(complete_prompt) + "\n\n")
            print(f"Test {iteration}.{i} completed")
        log.write("------------------------------------------------------------------\n")
        log.close()

def main():
    prompt_generation = TestPromptGeneration()
    request_list = [
        "all information on users who paid for their orders with PayPal",
        "all information about products that belong to an order placed by a user whose first name is alex"
    ]
    print("Test di generazione del prompt:\n")
    for i, request in enumerate(request_list):
        prompt_generation.iterate_prompt_generation(i, request)  

if __name__ == '__main__':
    main()