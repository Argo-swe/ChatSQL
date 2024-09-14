import time
from typing import List
from core.port.outcoming.embeddings.search_algorithm_port import SearchAlgorithmPort
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort


class TxtaiSearchAlgorithmAdapter(SearchAlgorithmPort):
    def __init__(self, index_manager: IndexManagerPort):
        self._index_manager = index_manager

    def semantic_search(self, user_request: str, activate_log: bool):
        """Execute an SQL-like query using txtai to perform semantic search on table and column description fields.

        Args:
            user_request (str): The user's query string, which is used to search for relevant matches.
            activate_log (bool): Flag indicating whether to log the details of the semantic search process.

        Returns:
            tuple:
                - The results of the semantic search.
                - A list of log entries (if logging is enabled), otherwise an empty list.
        """
        query_limit = 20
        # The max_score field can vary from 0.3 to 0.4. This affects system recall
        sql_query = f"""
            SELECT table_name, text, table_pos, column_description, MAX(score) AS max_score, AVG(score) AS avg_score
            FROM txtai WHERE
            similar(':x', 'table_description') AND
            similar(':x', 'column_description') AND
            score >= 0.2
            GROUP BY table_name
            HAVING max_score >= 0.35
            ORDER BY max_score DESC
            LIMIT {query_limit}
        """
        tuples = self._index_manager.get_embeddings().search(
            sql_query, limit=query_limit * 10, parameters={"x": user_request}
        )
        log_content = []
        if activate_log:
            log_content = self._semantic_search_log(user_request, tuples)
        return tuples, log_content

    def search_filtering(self, tuples: list, activate_log: bool):
        """Filters the tuples to find the most relevant ones based on their scores.

        Args:
            tuples (list): The tuples to filter.
            activate_log (bool): A flag to indicate whether the filtering process should be logged.

        Returns:
            tuple:
                - A list of tuples that have been deemed relevant based on score thresholds.
                - A list of log entries (if logging is enabled), otherwise an empty list.
        """
        relevant_tuples = []
        score = 0
        log_content = []
        for tuple in tuples:
            scoring_distance = score - tuple["max_score"]
            if tuple["max_score"] >= 0.45:
                relevant_tuples.append(tuple)
                score = tuple["max_score"]
            # The scoring_distance variable can vary from 0.15 to 0.25. This affects system recall
            elif scoring_distance <= 0.2:
                relevant_tuples.append(tuple)
            else:
                break
        if activate_log:
            log_content = self._search_filtering_log(relevant_tuples, tuples)

        return relevant_tuples, log_content

    def _semantic_search_log(self, user_request: str, tuples: list) -> List[str]:
        """Log the details of a semantic search operation.

        Args:
            user_request (str): The user's search query or request.
            tuples (list): A list of tuples representing the search results or related data.

        Returns:
            List[str]: A list of log entries detailing the semantic search process.
        """
        log_content = []
        log_content.append(
            f"{self.__get_debug_header()} - Details of the semantic search process.\n"
        )
        log_content.append(f"Request: {user_request}\n\n")
        log_content.append(
            f"{self.__get_debug_header()} - Phase 1 - first extraction\n"
        )
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
            token_importance = self._index_manager.get_embeddings().explain(
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
            token_importance = self._index_manager.get_embeddings().explain(
                user_request, [tuple["column_description"]], limit=1
            )[0]
            for token, score in sorted(
                token_importance["tokens"], key=lambda x: x[1], reverse=True
            ):
                log_content.append(token + ": " + str(score) + "\n")
            log_content.append("\n")
        return log_content

    def _search_filtering_log(self, relevant_tuples: list, tuples: list) -> List[str]:
        """Log the details of a filtering process using a custom algorithm.

        Args:
            relevant_tuples (list): A list of tuples representing the results deemed relevant by the custom algorithm.
            tuples (list): A list of all tuples considered during the search.

        Returns:
            List[str]: A list of log entries detailing the semantic search process.
        """
        log_content = []
        log_content.append(
            f"{self.__get_debug_header()} - Phase 2 - second extraction\n"
        )
        log_content.append("List of pertinent tables:\n")
        if not tuples:
            log_content.append("No tables found.\n\n")
        score = 0
        for tuple in relevant_tuples:
            scoring_distance = score - tuple["max_score"]
            if tuple["max_score"] >= 0.45:
                log_content.append(
                    f'The table {tuple["table_name"]} is kept because it has a high score.\n'
                )
                score = tuple["max_score"]
            elif scoring_distance <= 0.2:
                log_content.append(
                    f'The table {tuple["table_name"]} is kept because the score difference with the previous highly relevant table is less than 0.2 or the global score range is between 0.35 and 0.45.\n'
                )
            else:
                log_content.append(
                    "The remaining tables are discarded because the score is not high enough and the score difference with the previous highly relevant tables is greater than 0.2.\n"
                )
                break
        return log_content

    def __get_debug_header(self, level="DEBUG", system="ChatSQL"):
        """Generate a formatted debug header string.

        Args:
            level (str): The severity level of the log message.
            system (str): The name of the system generating the log.

        Returns:
            str: A formatted string suitable for use as a log header.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return f"[{timestamp}] [{system}] [{level}]"
