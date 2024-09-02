import type {
  AxiosRequestConfig,
  OpenAPIClient,
  OperationResponse,
  Parameters,
  UnknownParamsObject
} from 'openapi-client-axios';

declare namespace Components {
  namespace Schemas {
    /**
     * AuthResponseDto
     */
    export interface AuthResponseDto {
      /**
       * Message
       */
      message?: /* Message */ string | null;
      status: /* ResponseStatusEnum */ ResponseStatusEnum;
      /**
       * Data
       */
      data: /* Data */ {
        [key: string]: any;
      } | null;
    }
    /**
     * Body_createDictionary_api_dictionary__post
     */
    export interface BodyCreateDictionaryApiDictionaryPost {
      /**
       * File
       */
      file: string; // binary
    }
    /**
     * Body_updateDictionaryFile_api_dictionary__id__file_put
     */
    export interface BodyUpdateDictionaryFileApiDictionaryIdFilePut {
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
     * DictionaryPreviewDto
     */
    export interface DictionaryPreviewDto {
      /**
       * Databasename
       */
      databaseName: string;
      /**
       * Databasedescription
       */
      databaseDescription: string;
      /**
       * Tables
       */
      tables: /* TableDto */ TableDto[];
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
      /**
       * Data
       */
      data?: /* Data */ /* DictionaryDto */
      DictionaryDto | /* DictionaryPreviewDto */ DictionaryPreviewDto | null;
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
     * LoginDto
     */
    export interface LoginDto {
      /**
       * Username
       */
      username: string;
      /**
       * Password
       */
      password: string;
    }
    /**
     * PromptDto
     */
    export interface PromptDto {
      /**
       * Prompt
       */
      prompt?: /* Prompt */ string | null;
      /**
       * Debug
       */
      debug?: /* Debug */ string | null;
    }
    /**
     * PromptResponseDto
     */
    export interface PromptResponseDto {
      /**
       * Message
       */
      message?: /* Message */ string | null;
      status: /* ResponseStatusEnum */ ResponseStatusEnum;
      data: /* PromptDto */ PromptDto | null;
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
    export type ResponseStatusEnum =
      | 'OK'
      | 'ERROR'
      | 'BAD_CREDENTIAL'
      | 'BAD_REQUEST'
      | 'CONTENT_TOO_LARGE'
      | 'NOT_FOUND'
      | 'CONFLICT';
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
      data?: /* Data */ string | null;
    }
    /**
     * TableDto
     */
    export interface TableDto {
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
  namespace CreateDictionary {
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
      /**
       * Summary
       */
      export type Summary = any;
    }
    export interface QueryParameters {
      summary?: /* Summary */ Parameters.Summary;
      id?: /* Id */ Parameters.Id;
      name: /* Name */ Parameters.Name;
      description: /* Description */ Parameters.Description;
    }
    export type RequestBody =
      /* Body_createDictionary_api_dictionary__post */ Components.Schemas.BodyCreateDictionaryApiDictionaryPost;
    namespace Responses {
      export type $200 = /* DictionaryResponseDto */ Components.Schemas.DictionaryResponseDto;
      export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
    }
  }
  namespace DeleteDictionary {
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
  namespace GeneratePrompt {
    namespace Parameters {
      /**
       * Dbms
       */
      export type Dbms = string;
      /**
       * Dictionaryid
       */
      export type DictionaryId = number;
      /**
       * Lang
       */
      export type Lang = string;
      /**
       * Query
       */
      export type Query = string;
    }
    export interface QueryParameters {
      dictionaryId: /* Dictionaryid */ Parameters.DictionaryId;
      query: /* Query */ Parameters.Query;
      dbms: /* Dbms */ Parameters.Dbms;
      lang: /* Lang */ Parameters.Lang;
    }
    namespace Responses {
      export type $200 = /* StringDataResponseDto */ Components.Schemas.StringDataResponseDto;
      export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
    }
  }
  namespace GeneratePromptWithDebug {
    namespace Parameters {
      /**
       * Dbms
       */
      export type Dbms = string;
      /**
       * Dictionaryid
       */
      export type DictionaryId = number;
      /**
       * Lang
       */
      export type Lang = string;
      /**
       * Query
       */
      export type Query = string;
    }
    export interface QueryParameters {
      dictionaryId: /* Dictionaryid */ Parameters.DictionaryId;
      query: /* Query */ Parameters.Query;
      dbms: /* Dbms */ Parameters.Dbms;
      lang: /* Lang */ Parameters.Lang;
    }
    namespace Responses {
      export type $200 = /* PromptResponseDto */ Components.Schemas.PromptResponseDto;
      export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
    }
  }
  namespace GetAllDictionaries {
    namespace Responses {
      export type $200 = /* DictionariesResponseDto */ Components.Schemas.DictionariesResponseDto;
    }
  }
  namespace GetDictionary {
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
  namespace GetDictionaryFile {
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
  namespace GetDictionaryPreview {
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
  namespace Healthcheck {
    namespace Responses {
      export type $200 = any;
    }
  }
  namespace Login {
    export type RequestBody = /* LoginDto */ Components.Schemas.LoginDto;
    namespace Responses {
      export type $200 = /* AuthResponseDto */ Components.Schemas.AuthResponseDto;
      export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
    }
  }
  namespace Main {
    namespace Responses {
      export type $200 = any;
    }
  }
  namespace UpdateDictionaryFile {
    namespace Parameters {
      /**
       * Id
       */
      export type Id = number;
    }
    export interface PathParameters {
      id: /* Id */ Parameters.Id;
    }
    export type RequestBody =
      /* Body_updateDictionaryFile_api_dictionary__id__file_put */ Components.Schemas.BodyUpdateDictionaryFileApiDictionaryIdFilePut;
    namespace Responses {
      export type $200 = /* DictionaryResponseDto */ Components.Schemas.DictionaryResponseDto;
      export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
    }
  }
  namespace UpdateDictionaryMetadata {
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
   * getAllDictionaries - Retrieve all dictionaries
   *
   * Retrieve a list of all dictionaries available in the system.
   */
  'getAllDictionaries'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: any,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.GetAllDictionaries.Responses.$200>;
  /**
   * createDictionary - Createdictionary
   *
   * Create a new dictionary with metadata and an optional file.
   */
  'createDictionary'(
    parameters?: Parameters<Paths.CreateDictionary.QueryParameters> | null,
    data?: Paths.CreateDictionary.RequestBody,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.CreateDictionary.Responses.$200>;
  /**
   * getDictionary - Retrieve a dictionary by ID
   *
   * Retrieve the details of a specific dictionary by its ID.
   */
  'getDictionary'(
    parameters?: Parameters<Paths.GetDictionary.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.GetDictionary.Responses.$200>;
  /**
   * updateDictionaryMetadata - Update dictionary metadata by ID
   *
   * Update the metadata of a specific dictionary by its ID.
   */
  'updateDictionaryMetadata'(
    parameters?: Parameters<Paths.UpdateDictionaryMetadata.PathParameters> | null,
    data?: Paths.UpdateDictionaryMetadata.RequestBody,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.UpdateDictionaryMetadata.Responses.$200>;
  /**
   * deleteDictionary - Delete a dictionary by ID
   *
   * Delete a specific dictionary by its ID.
   */
  'deleteDictionary'(
    parameters?: Parameters<Paths.DeleteDictionary.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.DeleteDictionary.Responses.$200>;
  /**
   * getDictionaryFile - Download a dictionary file by ID
   *
   * Download the file associated with a specific dictionary by its ID.
   */
  'getDictionaryFile'(
    parameters?: Parameters<Paths.GetDictionaryFile.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.GetDictionaryFile.Responses.$200>;
  /**
   * updateDictionaryFile - Update dictionary file by ID
   *
   * Update the file associated with a specific dictionary by its ID.
   */
  'updateDictionaryFile'(
    parameters?: Parameters<Paths.UpdateDictionaryFile.PathParameters> | null,
    data?: Paths.UpdateDictionaryFile.RequestBody,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.UpdateDictionaryFile.Responses.$200>;
  /**
   * getDictionaryPreview - Retrieve a dictionary preview by ID
   *
   * Retrieve a preview of a specific dictionary by its ID.
   */
  'getDictionaryPreview'(
    parameters?: Parameters<Paths.GetDictionaryPreview.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.GetDictionaryPreview.Responses.$200>;
  /**
   * generatePrompt - Generate a prompt based on query parameters
   *
   * Generate a prompt using the provided parameters.
   *
   * - **dictionaryId**: ID of the dictionary to be used.
   * - **query**: The input query string to generate the prompt.
   * - **dbms**: The database management system being used.
   * - **lang**: The language for the generated prompt.
   *
   * Returns the generated prompt as a string.
   */
  'generatePrompt'(
    parameters?: Parameters<Paths.GeneratePrompt.QueryParameters> | null,
    data?: any,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.GeneratePrompt.Responses.$200>;
  /**
   * generatePromptWithDebug - Generate a prompt with debug information
   *
   * Generate a prompt with detailed debug information.
   *
   * - **dictionaryId**: ID of the dictionary to be used.
   * - **query**: The input query string to generate the prompt.
   * - **dbms**: The database management system being used.
   * - **lang**: The language for the generated prompt.
   *
   * Returns the generated prompt along with additional debug data.
   */
  'generatePromptWithDebug'(
    parameters?: Parameters<Paths.GeneratePromptWithDebug.QueryParameters> | null,
    data?: any,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.GeneratePromptWithDebug.Responses.$200>;
  /**
   * login - User login
   *
   * Authenticate a user with the provided credentials.
   *
   * - **username**: The username of the user.
   * - **password**: The password of the user.
   *
   * Returns an authentication token if the login is successful.
   */
  'login'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: Paths.Login.RequestBody,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.Login.Responses.$200>;
  /**
   * main - Root endpoint
   *
   * Return a simple greeting message.
   *
   * This endpoint can be used to verify that the API is reachable.
   */
  'main'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: any,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.Main.Responses.$200>;
  /**
   * healthcheck - Health check endpoint
   *
   * Check the health status of the API.
   *
   * Returns a status message indicating whether the API is running.
   */
  'healthcheck'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: any,
    config?: AxiosRequestConfig
  ): OperationResponse<Paths.Healthcheck.Responses.$200>;
}

export interface PathsDictionary {
  ['/api/dictionary/']: {
    /**
     * getAllDictionaries - Retrieve all dictionaries
     *
     * Retrieve a list of all dictionaries available in the system.
     */
    'get'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: any,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.GetAllDictionaries.Responses.$200>;
    /**
     * createDictionary - Createdictionary
     *
     * Create a new dictionary with metadata and an optional file.
     */
    'post'(
      parameters?: Parameters<Paths.CreateDictionary.QueryParameters> | null,
      data?: Paths.CreateDictionary.RequestBody,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.CreateDictionary.Responses.$200>;
  };
  ['/api/dictionary/{id}']: {
    /**
     * getDictionary - Retrieve a dictionary by ID
     *
     * Retrieve the details of a specific dictionary by its ID.
     */
    'get'(
      parameters?: Parameters<Paths.GetDictionary.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.GetDictionary.Responses.$200>;
    /**
     * updateDictionaryMetadata - Update dictionary metadata by ID
     *
     * Update the metadata of a specific dictionary by its ID.
     */
    'put'(
      parameters?: Parameters<Paths.UpdateDictionaryMetadata.PathParameters> | null,
      data?: Paths.UpdateDictionaryMetadata.RequestBody,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.UpdateDictionaryMetadata.Responses.$200>;
    /**
     * deleteDictionary - Delete a dictionary by ID
     *
     * Delete a specific dictionary by its ID.
     */
    'delete'(
      parameters?: Parameters<Paths.DeleteDictionary.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.DeleteDictionary.Responses.$200>;
  };
  ['/api/dictionary/{id}/file']: {
    /**
     * getDictionaryFile - Download a dictionary file by ID
     *
     * Download the file associated with a specific dictionary by its ID.
     */
    'get'(
      parameters?: Parameters<Paths.GetDictionaryFile.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.GetDictionaryFile.Responses.$200>;
    /**
     * updateDictionaryFile - Update dictionary file by ID
     *
     * Update the file associated with a specific dictionary by its ID.
     */
    'put'(
      parameters?: Parameters<Paths.UpdateDictionaryFile.PathParameters> | null,
      data?: Paths.UpdateDictionaryFile.RequestBody,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.UpdateDictionaryFile.Responses.$200>;
  };
  ['/api/dictionary/{id}/dictionary-preview']: {
    /**
     * getDictionaryPreview - Retrieve a dictionary preview by ID
     *
     * Retrieve a preview of a specific dictionary by its ID.
     */
    'get'(
      parameters?: Parameters<Paths.GetDictionaryPreview.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.GetDictionaryPreview.Responses.$200>;
  };
  ['/api/prompt/']: {
    /**
     * generatePrompt - Generate a prompt based on query parameters
     *
     * Generate a prompt using the provided parameters.
     *
     * - **dictionaryId**: ID of the dictionary to be used.
     * - **query**: The input query string to generate the prompt.
     * - **dbms**: The database management system being used.
     * - **lang**: The language for the generated prompt.
     *
     * Returns the generated prompt as a string.
     */
    'get'(
      parameters?: Parameters<Paths.GeneratePrompt.QueryParameters> | null,
      data?: any,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.GeneratePrompt.Responses.$200>;
  };
  ['/api/prompt/debug']: {
    /**
     * generatePromptWithDebug - Generate a prompt with debug information
     *
     * Generate a prompt with detailed debug information.
     *
     * - **dictionaryId**: ID of the dictionary to be used.
     * - **query**: The input query string to generate the prompt.
     * - **dbms**: The database management system being used.
     * - **lang**: The language for the generated prompt.
     *
     * Returns the generated prompt along with additional debug data.
     */
    'get'(
      parameters?: Parameters<Paths.GeneratePromptWithDebug.QueryParameters> | null,
      data?: any,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.GeneratePromptWithDebug.Responses.$200>;
  };
  ['/api/login/']: {
    /**
     * login - User login
     *
     * Authenticate a user with the provided credentials.
     *
     * - **username**: The username of the user.
     * - **password**: The password of the user.
     *
     * Returns an authentication token if the login is successful.
     */
    'post'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: Paths.Login.RequestBody,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.Login.Responses.$200>;
  };
  ['/']: {
    /**
     * main - Root endpoint
     *
     * Return a simple greeting message.
     *
     * This endpoint can be used to verify that the API is reachable.
     */
    'get'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: any,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.Main.Responses.$200>;
  };
  ['/healthcheck']: {
    /**
     * healthcheck - Health check endpoint
     *
     * Check the health status of the API.
     *
     * Returns a status message indicating whether the API is running.
     */
    'get'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: any,
      config?: AxiosRequestConfig
    ): OperationResponse<Paths.Healthcheck.Responses.$200>;
  };
}

export type Client = OpenAPIClient<OperationMethods, PathsDictionary>;
