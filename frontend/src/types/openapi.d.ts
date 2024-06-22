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
        }
        export interface QueryParameters {
            id?: /* Id */ Parameters.Id;
            name: /* Name */ Parameters.Name;
            description: /* Description */ Parameters.Description;
        }
        export type RequestBody = /* Body_createDictionary_api_dictionary__post */ Components.Schemas.BodyCreateDictionaryApiDictionaryPost;
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
    namespace GeneratePromptDebug {
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
        export type RequestBody = /* Body_updateDictionaryFile_api_dictionary__id__file_put */ Components.Schemas.BodyUpdateDictionaryFileApiDictionaryIdFilePut;
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
   * getAllDictionaries - Getalldictionaries
   */
  'getAllDictionaries'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GetAllDictionaries.Responses.$200>
  /**
   * createDictionary - Createdictionary
   */
  'createDictionary'(
    parameters?: Parameters<Paths.CreateDictionary.QueryParameters> | null,
    data?: Paths.CreateDictionary.RequestBody,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.CreateDictionary.Responses.$200>
  /**
   * getDictionary - Getdictionary
   */
  'getDictionary'(
    parameters?: Parameters<Paths.GetDictionary.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GetDictionary.Responses.$200>
  /**
   * updateDictionaryMetadata - Updatedictionarymetadata
   */
  'updateDictionaryMetadata'(
    parameters?: Parameters<Paths.UpdateDictionaryMetadata.PathParameters> | null,
    data?: Paths.UpdateDictionaryMetadata.RequestBody,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.UpdateDictionaryMetadata.Responses.$200>
  /**
   * deleteDictionary - Deletedictionary
   */
  'deleteDictionary'(
    parameters?: Parameters<Paths.DeleteDictionary.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.DeleteDictionary.Responses.$200>
  /**
   * getDictionaryFile - Getdictionaryfile
   */
  'getDictionaryFile'(
    parameters?: Parameters<Paths.GetDictionaryFile.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GetDictionaryFile.Responses.$200>
  /**
   * updateDictionaryFile - Updatedictionaryfile
   */
  'updateDictionaryFile'(
    parameters?: Parameters<Paths.UpdateDictionaryFile.PathParameters> | null,
    data?: Paths.UpdateDictionaryFile.RequestBody,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.UpdateDictionaryFile.Responses.$200>
  /**
   * generatePrompt - Generateprompt
   */
  'generatePrompt'(
    parameters?: Parameters<Paths.GeneratePrompt.QueryParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GeneratePrompt.Responses.$200>
  /**
   * generatePromptDebug - Generatepromptdebug
   */
  'generatePromptDebug'(
    parameters?: Parameters<Paths.GeneratePromptDebug.QueryParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GeneratePromptDebug.Responses.$200>
  /**
   * login - Login
   */
  'login'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: Paths.Login.RequestBody,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.Login.Responses.$200>
  /**
   * main - Main
   */
  'main'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.Main.Responses.$200>
}

export interface PathsDictionary {
  ['/api/dictionary/']: {
    /**
     * getAllDictionaries - Getalldictionaries
     */
    'get'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GetAllDictionaries.Responses.$200>
    /**
     * createDictionary - Createdictionary
     */
    'post'(
      parameters?: Parameters<Paths.CreateDictionary.QueryParameters> | null,
      data?: Paths.CreateDictionary.RequestBody,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.CreateDictionary.Responses.$200>
  }
  ['/api/dictionary/{id}']: {
    /**
     * getDictionary - Getdictionary
     */
    'get'(
      parameters?: Parameters<Paths.GetDictionary.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GetDictionary.Responses.$200>
    /**
     * updateDictionaryMetadata - Updatedictionarymetadata
     */
    'put'(
      parameters?: Parameters<Paths.UpdateDictionaryMetadata.PathParameters> | null,
      data?: Paths.UpdateDictionaryMetadata.RequestBody,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.UpdateDictionaryMetadata.Responses.$200>
    /**
     * deleteDictionary - Deletedictionary
     */
    'delete'(
      parameters?: Parameters<Paths.DeleteDictionary.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.DeleteDictionary.Responses.$200>
  }
  ['/api/dictionary/{id}/file']: {
    /**
     * getDictionaryFile - Getdictionaryfile
     */
    'get'(
      parameters?: Parameters<Paths.GetDictionaryFile.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GetDictionaryFile.Responses.$200>
    /**
     * updateDictionaryFile - Updatedictionaryfile
     */
    'put'(
      parameters?: Parameters<Paths.UpdateDictionaryFile.PathParameters> | null,
      data?: Paths.UpdateDictionaryFile.RequestBody,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.UpdateDictionaryFile.Responses.$200>
  }
  ['/api/prompt/']: {
    /**
     * generatePrompt - Generateprompt
     */
    'get'(
      parameters?: Parameters<Paths.GeneratePrompt.QueryParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GeneratePrompt.Responses.$200>
  }
  ['/api/prompt/debug']: {
    /**
     * generatePromptDebug - Generatepromptdebug
     */
    'get'(
      parameters?: Parameters<Paths.GeneratePromptDebug.QueryParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GeneratePromptDebug.Responses.$200>
  }
  ['/api/login/']: {
    /**
     * login - Login
     */
    'post'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: Paths.Login.RequestBody,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.Login.Responses.$200>
  }
  ['/']: {
    /**
     * main - Main
     */
    'get'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.Main.Responses.$200>
  }
}

export type Client = OpenAPIClient<OperationMethods, PathsDictionary>

