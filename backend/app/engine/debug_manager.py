import time
from pathlib import Path
import os

logs_file_out_file_base_path = "/opt/chatsql/logs/chatsql_log.txt"
os.makedirs(Path(logs_file_out_file_base_path).parent, exist_ok=True)


class DebugManager:
    def __init__(self, embeddings):
        self.embeddings = embeddings

    def semantic_search_log(self, user_request, tuples):
        log_content = []
        log_content.append(
            f"{self.get_debug_header()} - Details of the prompt generation process.\n"
        )
        log_content.append(f"Request: {user_request}\n\n")
        log_content.append(f"{self.get_debug_header()} - Phase 1 - first extraction\n")
        log_content.append("List of relevant tables:\n")
        if not tuples:
            log_content.append("No relevant tables found.\n")
        log_content.append("\n")
        for i, tuple in enumerate(tuples):
            log_content.append(
                f'Table {i + 1} | {tuple["table_name"]}: {tuple["max_score"]}\n'
            )
            log_content.append(f'Description of the table: {tuple["text"]}\n')
            log_content.append(
                "Ranking of the most relevant terms in the description:\n"
            )
            token_importance = self.embeddings.explain(
                user_request, [tuple["text"]], limit=1
            )[0]
            for token, score in sorted(
                token_importance["tokens"], key=lambda x: x[1], reverse=True
            ):
                log_content.append(token + ": " + str(score) + "\n")
            log_content.append(
                f'\nDescription of the most relevant column: {tuple["column_description"]}\n'
            )
            log_content.append(
                "Ranking of the most relevant terms in the description:\n"
            )
            token_importance = self.embeddings.explain(
                user_request, [tuple["column_description"]], limit=1
            )[0]
            for token, score in sorted(
                token_importance["tokens"], key=lambda x: x[1], reverse=True
            ):
                log_content.append(token + ": " + str(score) + "\n")
            log_content.append("\n")
        return log_content

    def get_debug_header(self, level="DEBUG", system="ChatSQL"):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return f"[{timestamp}] [{system}] [{level}]"

    def log_phase_2(self, relevant_tuples, tuples):
        log_content = []
        log_content.append(f"{self.get_debug_header()} - Phase 2 - second extraction\n")
        log_content.append("List of pertinent tables:\n")
        if not tuples:
            log_content.append("No tables found.\n\n")
        score = 0
        for tuple in relevant_tuples:
            scoring_distance = score - tuple["max_score"]
            if tuple["max_score"] >= 0.45:
                log_content.append(
                    f'The table {tuple["table_name"]} is kept because it has a sufficiently high score.\n'
                )
                score = tuple["max_score"]
            elif scoring_distance <= 0.25:
                log_content.append(
                    f'The table {tuple["table_name"]} is kept because the score difference with the previous table is less than 0.25.\n'
                )
                score = tuple["max_score"]
            else:
                log_content.append(
                    "The remaining tables are discarded because the score is not high enough and the score difference with the previous tables is greater than 0.25.\n"
                )
                break
        return log_content
