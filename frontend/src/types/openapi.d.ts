import type {
  OpenAPIClient,
  Parameters,
  UnknownParamsObject,
  OperationResponse,
  AxiosRequestConfig,
} from 'openapi-client-axios';

declare namespace Components {
    namespace Schemas {
        /**
         * Body_create_dictionary_api_dictionary__post
         */
        export interface BodyCreateDictionaryApiDictionaryPost {
            /**
             * File
             */
            file: string; // binary
        }
        /**
         * Body_update_dicrionary_file_api_dictionary__id__file_put
         */
        export interface BodyUpdateDicrionaryFileApiDictionaryIdFilePut {
            /**
             * File
             */
            file: string; // binary
        }
        /**
         * DictionariesResponseDto
         */
        export interface DictionariesResponseDto {
            /**
             * Message
             */
            message?: /* Message */ string | null;
            status: /* ResponseStatusEnum */ ResponseStatusEnum;
            /**
             * Data
             */
            data: /* Data */ /* DictionaryDto */ DictionaryDto[] | null[];
        }
        /**
         * DictionaryDto
         */
        export interface DictionaryDto {
            /**
             * Id
             */
            id?: /* Id */ number | null;
            /**
             * Name
             */
            name: string;
            /**
             * Description
             */
            description: string;
        }
        /**
         * DictionaryResponseDto
         */
        export interface DictionaryResponseDto {
            /**
             * Message
             */
            message?: /* Message */ string | null;
            status: /* ResponseStatusEnum */ ResponseStatusEnum;
            data: /* DictionaryDto */ DictionaryDto | null;
        }
        /**
         * HTTPValidationError
         */
        export interface HTTPValidationError {
            /**
             * Detail
             */
            detail?: /* ValidationError */ ValidationError[];
        }
        /**
         * ResponseDto
         */
        export interface ResponseDto {
            /**
             * Message
             */
            message?: /* Message */ string | null;
            status: /* ResponseStatusEnum */ ResponseStatusEnum;
        }
        /**
         * ResponseStatusEnum
         */
        export type ResponseStatusEnum = "OK" | "ERROR" | "BAD_REQUEST" | "NOT_FOUND";
        /**
         * StringDataResponseDto
         */
        export interface StringDataResponseDto {
            /**
             * Message
             */
            message?: /* Message */ string | null;
            status: /* ResponseStatusEnum */ ResponseStatusEnum;
            /**
             * Data
             */
            data: string;
        }
        /**
         * ValidationError
         */
        export interface ValidationError {
            /**
             * Location
             */
            loc: (string | number)[];
            /**
             * Message
             */
            msg: string;
            /**
             * Error Type
             */
            type: string;
        }
    }
}
declare namespace Paths {
    namespace CreateDictionaryApiDictionaryPost {
        namespace Parameters {
            /**
             * Description
             */
            export type Description = string;
            /**
             * Id
             */
            export type Id = /* Id */ number | null;
            /**
             * Name
             */
            export type Name = string;
        }
        export interface QueryParameters {
            id?: /* Id */ Parameters.Id;
            name: /* Name */ Parameters.Name;
            description: /* Description */ Parameters.Description;
        }
        export type RequestBody = /* Body_create_dictionary_api_dictionary__post */ Components.Schemas.BodyCreateDictionaryApiDictionaryPost;
        namespace Responses {
            export type $200 = /* DictionaryResponseDto */ Components.Schemas.DictionaryResponseDto;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace DeleteDicrionaryApiDictionaryIdDelete {
        namespace Parameters {
            /**
             * Id
             */
            export type Id = number;
        }
        export interface PathParameters {
            id: /* Id */ Parameters.Id;
        }
        namespace Responses {
            export type $200 = /* ResponseDto */ Components.Schemas.ResponseDto;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace GeneratePromptApiPromptDebugGet {
        namespace Parameters {
            /**
             * Query
             */
            export type Query = string;
        }
        export interface QueryParameters {
            query: /* Query */ Parameters.Query;
        }
        namespace Responses {
            export type $200 = /* StringDataResponseDto */ Components.Schemas.StringDataResponseDto;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace GeneratePromptApiPromptGet {
        namespace Parameters {
            /**
             * Query
             */
            export type Query = string;
        }
        export interface QueryParameters {
            query: /* Query */ Parameters.Query;
        }
        namespace Responses {
            export type $200 = /* StringDataResponseDto */ Components.Schemas.StringDataResponseDto;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace GetAllDictionariesApiDictionaryGet {
        namespace Responses {
            export type $200 = /* DictionariesResponseDto */ Components.Schemas.DictionariesResponseDto;
        }
    }
    namespace GetDictionaryApiDictionaryIdGet {
        namespace Parameters {
            /**
             * Id
             */
            export type Id = number;
        }
        export interface PathParameters {
            id: /* Id */ Parameters.Id;
        }
        namespace Responses {
            export type $200 = /* DictionaryResponseDto */ Components.Schemas.DictionaryResponseDto;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace GetDictionaryFileApiDictionaryIdFileGet {
        namespace Parameters {
            /**
             * Id
             */
            export type Id = number;
        }
        export interface PathParameters {
            id: /* Id */ Parameters.Id;
        }
        namespace Responses {
            export type $200 = any;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace MainGet {
        namespace Responses {
            export type $200 = any;
        }
    }
    namespace UpdateDicrionaryFileApiDictionaryIdFilePut {
        namespace Parameters {
            /**
             * Id
             */
            export type Id = number;
        }
        export interface PathParameters {
            id: /* Id */ Parameters.Id;
        }
        export type RequestBody = /* Body_update_dicrionary_file_api_dictionary__id__file_put */ Components.Schemas.BodyUpdateDicrionaryFileApiDictionaryIdFilePut;
        namespace Responses {
            export type $200 = /* DictionaryResponseDto */ Components.Schemas.DictionaryResponseDto;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace UpdateDicrionaryMetadataApiDictionaryIdPut {
        namespace Parameters {
            /**
             * Id
             */
            export type Id = number;
        }
        export interface PathParameters {
            id: /* Id */ Parameters.Id;
        }
        export type RequestBody = /* DictionaryDto */ Components.Schemas.DictionaryDto;
        namespace Responses {
            export type $200 = /* DictionaryResponseDto */ Components.Schemas.DictionaryResponseDto;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
}

export interface OperationMethods {
  /**
   * get_all_dictionaries_api_dictionary__get - Get All Dictionaries
   */
  'get_all_dictionaries_api_dictionary__get'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GetAllDictionariesApiDictionaryGet.Responses.$200>
  /**
   * create_dictionary_api_dictionary__post - Create Dictionary
   */
  'create_dictionary_api_dictionary__post'(
    parameters?: Parameters<Paths.CreateDictionaryApiDictionaryPost.QueryParameters> | null,
    data?: Paths.CreateDictionaryApiDictionaryPost.RequestBody,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.CreateDictionaryApiDictionaryPost.Responses.$200>
  /**
   * get_dictionary_api_dictionary__id__get - Get Dictionary
   */
  'get_dictionary_api_dictionary__id__get'(
    parameters?: Parameters<Paths.GetDictionaryApiDictionaryIdGet.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GetDictionaryApiDictionaryIdGet.Responses.$200>
  /**
   * update_dicrionary_metadata_api_dictionary__id__put - Update Dicrionary Metadata
   */
  'update_dicrionary_metadata_api_dictionary__id__put'(
    parameters?: Parameters<Paths.UpdateDicrionaryMetadataApiDictionaryIdPut.PathParameters> | null,
    data?: Paths.UpdateDicrionaryMetadataApiDictionaryIdPut.RequestBody,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.UpdateDicrionaryMetadataApiDictionaryIdPut.Responses.$200>
  /**
   * delete_dicrionary_api_dictionary__id__delete - Delete Dicrionary
   */
  'delete_dicrionary_api_dictionary__id__delete'(
    parameters?: Parameters<Paths.DeleteDicrionaryApiDictionaryIdDelete.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.DeleteDicrionaryApiDictionaryIdDelete.Responses.$200>
  /**
   * get_dictionary_file_api_dictionary__id__file_get - Get Dictionary File
   */
  'get_dictionary_file_api_dictionary__id__file_get'(
    parameters?: Parameters<Paths.GetDictionaryFileApiDictionaryIdFileGet.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GetDictionaryFileApiDictionaryIdFileGet.Responses.$200>
  /**
   * update_dicrionary_file_api_dictionary__id__file_put - Update Dicrionary File
   */
  'update_dicrionary_file_api_dictionary__id__file_put'(
    parameters?: Parameters<Paths.UpdateDicrionaryFileApiDictionaryIdFilePut.PathParameters> | null,
    data?: Paths.UpdateDicrionaryFileApiDictionaryIdFilePut.RequestBody,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.UpdateDicrionaryFileApiDictionaryIdFilePut.Responses.$200>
  /**
   * generate_prompt_api_prompt__get - Generate Prompt
   */
  'generate_prompt_api_prompt__get'(
    parameters?: Parameters<Paths.GeneratePromptApiPromptGet.QueryParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GeneratePromptApiPromptGet.Responses.$200>
  /**
   * generate_prompt_api_prompt_debug_get - Generate Prompt
   */
  'generate_prompt_api_prompt_debug_get'(
    parameters?: Parameters<Paths.GeneratePromptApiPromptDebugGet.QueryParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GeneratePromptApiPromptDebugGet.Responses.$200>
  /**
   * main__get - Main
   */
  'main__get'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.MainGet.Responses.$200>
}

export interface PathsDictionary {
  ['/api/dictionary/']: {
    /**
     * get_all_dictionaries_api_dictionary__get - Get All Dictionaries
     */
    'get'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GetAllDictionariesApiDictionaryGet.Responses.$200>
    /**
     * create_dictionary_api_dictionary__post - Create Dictionary
     */
    'post'(
      parameters?: Parameters<Paths.CreateDictionaryApiDictionaryPost.QueryParameters> | null,
      data?: Paths.CreateDictionaryApiDictionaryPost.RequestBody,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.CreateDictionaryApiDictionaryPost.Responses.$200>
  }
  ['/api/dictionary/{id}']: {
    /**
     * get_dictionary_api_dictionary__id__get - Get Dictionary
     */
    'get'(
      parameters?: Parameters<Paths.GetDictionaryApiDictionaryIdGet.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GetDictionaryApiDictionaryIdGet.Responses.$200>
    /**
     * update_dicrionary_metadata_api_dictionary__id__put - Update Dicrionary Metadata
     */
    'put'(
      parameters?: Parameters<Paths.UpdateDicrionaryMetadataApiDictionaryIdPut.PathParameters> | null,
      data?: Paths.UpdateDicrionaryMetadataApiDictionaryIdPut.RequestBody,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.UpdateDicrionaryMetadataApiDictionaryIdPut.Responses.$200>
    /**
     * delete_dicrionary_api_dictionary__id__delete - Delete Dicrionary
     */
    'delete'(
      parameters?: Parameters<Paths.DeleteDicrionaryApiDictionaryIdDelete.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.DeleteDicrionaryApiDictionaryIdDelete.Responses.$200>
  }
  ['/api/dictionary/{id}/file']: {
    /**
     * get_dictionary_file_api_dictionary__id__file_get - Get Dictionary File
     */
    'get'(
      parameters?: Parameters<Paths.GetDictionaryFileApiDictionaryIdFileGet.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GetDictionaryFileApiDictionaryIdFileGet.Responses.$200>
    /**
     * update_dicrionary_file_api_dictionary__id__file_put - Update Dicrionary File
     */
    'put'(
      parameters?: Parameters<Paths.UpdateDicrionaryFileApiDictionaryIdFilePut.PathParameters> | null,
      data?: Paths.UpdateDicrionaryFileApiDictionaryIdFilePut.RequestBody,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.UpdateDicrionaryFileApiDictionaryIdFilePut.Responses.$200>
  }
  ['/api/prompt/']: {
    /**
     * generate_prompt_api_prompt__get - Generate Prompt
     */
    'get'(
      parameters?: Parameters<Paths.GeneratePromptApiPromptGet.QueryParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GeneratePromptApiPromptGet.Responses.$200>
  }
  ['/api/prompt/debug']: {
    /**
     * generate_prompt_api_prompt_debug_get - Generate Prompt
     */
    'get'(
      parameters?: Parameters<Paths.GeneratePromptApiPromptDebugGet.QueryParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GeneratePromptApiPromptDebugGet.Responses.$200>
  }
  ['/']: {
    /**
     * main__get - Main
     */
    'get'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.MainGet.Responses.$200>
  }
}

export type Client = OpenAPIClient<OperationMethods, PathsDictionary>

