from adapter.outcoming.txtai.txtai_index_manager_adapter import TxtaiIndexManagerAdapter
from adapter.outcoming.txtai.txtai_debug_manager_agapter import TxtaiDebugManagerAdapter
from core.port.outcoming.prompt_manager_port import PromptManagerPort
from tools.schema_multi_extractor import SchemaMultiExtractor


class TxtaiPromptManagerAdapter(PromptManagerPort):
    def __init__(self, index_manager: TxtaiIndexManagerAdapter):
        self._index_manager = index_manager
        self._debug_manager = TxtaiDebugManagerAdapter(self._index_manager.embeddings)

    def prompt_generator(
        self,
        dictionary_id,
        user_request,
        lang="english",
        dbms="MariaDB",
        activate_log=False,
    ) -> tuple[str, str | None]:
        self._index_manager.load_index(dictionary_id)
        tuples, log_content_phase_1 = self.__get_tuples(user_request, activate_log)
        relevant_tuples, log_content_phase_2 = self.__get_relevant_tuples(
            tuples, activate_log
        )
        if not relevant_tuples:
            response = (
                f"""Sorry, the ChatBOT was unable to find any relevant results for "{user_request}".\n"""
                """We invite you to try again with a different request."""
            )
            log_content = "\n".join(log_content_phase_1) if activate_log else None
            return response, log_content
        schema = SchemaMultiExtractor.get_json_schema(dictionary_id)
        # TODO check schema is not None
        dyn_string = (
            "Suggested prompt:\n"
            "In table schema the character ':' separates the column name from its type\n"
            "Foreign keys have the following schema: table name (column name) references table name (column name)\n\n"
        )
        dyn_ref_string = "FOREIGN KEYS:\n"
        for table in relevant_tuples:
            table_schema = schema["tables"][table["table_pos"]]
            dyn_key_string = (
                f'PRIMARY KEY: ({", ".join(table_schema["primary_key"])})\n'
            )
            dyn_desc_string = (
                f'Table description: {table_schema["description"]}\n'
                "The table contains the following columns:\n"
            )
            column_def = [
                f'{column["name"]}: {column["type"]}'
                for column in table_schema["columns"]
            ]
            dyn_desc_string += "\n".join(
                f'{column["name"]}: {column["description"]}'
                for column in table_schema["columns"]
            )
            dyn_string += (
                f'Table schema: {table_schema["name"]} ({", ".join(column_def)})\n'
            )
            dyn_string += dyn_key_string
            dyn_string += dyn_desc_string + "\n"
            if "foreign_keys" in table_schema:
                for foreign_key in table_schema["foreign_keys"]:
                    dyn_ref_string += (
                        f'FOREIGN KEY {table_schema["name"]} ('
                        f'{", ".join(foreign_key["foreign_key_column_names"])}) references '
                        f'{foreign_key["reference_table_name"]} ('
                        f'{", ".join(foreign_key["reference_column_names"])})\n'
                    )
        dyn_string += dyn_ref_string + "\n"
        dyn_string += f"User request: {user_request}.\n"
        dyn_string += f"Convert user request to a suitable SQL query for {dbms}.\n"
        dyn_string += f"Answer in {lang}."
        log_content = (
            "\n".join(log_content_phase_1 + log_content_phase_2)
            if activate_log
            else None
        )
        return dyn_string, log_content

    def __get_tuples(self, user_request: str, activate_log: bool):
        query_limit = 20
        sql_query = f"""
            SELECT table_name, text, table_pos, column_description, MAX(score) AS max_score, AVG(score) AS avg_score
            FROM txtai WHERE
            similar(':x', 'table_description') AND
            similar(':x', 'column_description') AND
            score >= 0.2
            GROUP BY table_name
            HAVING max_score >= 0.3 OR avg_score >= 0.28
            ORDER BY max_score DESC
            LIMIT {query_limit}
        """
        tuples = self._index_manager.embeddings.search(
            sql_query, limit=query_limit * 10, parameters={"x": user_request}
        )
        log_content = None
        if activate_log:
            log_content = self._debug_manager.semantic_search_log(user_request, tuples)
        return tuples, log_content

    def __get_relevant_tuples(self, tuples, activate_log):
        relevant_tuples = []
        score = 0
        log_content = []
        for tuple in tuples:
            scoring_distance = score - tuple["max_score"]
            if tuple["max_score"] >= 0.45:
                relevant_tuples.append(tuple)
                score = tuple["max_score"]
            elif scoring_distance <= 0.25:
                relevant_tuples.append(tuple)
                score = tuple["max_score"]
            else:
                break
        if activate_log:
            log_content.extend(self._debug_manager.log_phase_2(relevant_tuples, tuples))
        return relevant_tuples, log_content
