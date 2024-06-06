import type {
  OpenAPIClient,
  Parameters,
  UnknownParamsObject,
  OperationResponse,
  AxiosRequestConfig,
} from 'openapi-client-axios';

declare namespace Paths {
    namespace ApiTest$TestId {
        namespace Parameters {
            export type TestId = number;
        }
        export interface PathParameters {
            test_id: Parameters.TestId;
        }
    }
}

export interface OperationMethods {
  /**
   * get_test
   */
  'get_test'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<any>
  /**
   * get_check_test
   */
  'get_check_test'(
    parameters?: Parameters<Paths.ApiTest$TestId.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<any>
  /**
   * post_check_test
   */
  'post_check_test'(
    parameters?: Parameters<Paths.ApiTest$TestId.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<any>
}

export interface PathsDictionary {
  ['/api/test/']: {
    /**
     * get_test
     */
    'get'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<any>
  }
  ['/api/test/{test_id}']: {
    /**
     * get_check_test
     */
    'get'(
      parameters?: Parameters<Paths.ApiTest$TestId.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<any>
    /**
     * post_check_test
     */
    'post'(
      parameters?: Parameters<Paths.ApiTest$TestId.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<any>
  }
}

export type Client = OpenAPIClient<OperationMethods, PathsDictionary>

