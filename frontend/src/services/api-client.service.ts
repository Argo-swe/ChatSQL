import { OpenAPIClientAxios } from 'openapi-client-axios';
import type { Client as ApiClient } from '../types/openapi';

/**
 * Manages the creation and retrieval of an API client.
 */
export default class ApiClientManager {
  private static api: OpenAPIClientAxios;
  private static client?: ApiClient;

  /**
   * Static block to initialize the OpenAPIClientAxios instance.
   */
  static {
    ApiClientManager.api = new OpenAPIClientAxios({
      definition: import.meta.env.VITE_OPENAPI_BASE_URL
    });
  }

  /**
   * Initializes (if necessary) and retrieves the API client.
   * Automatically attaches the token from localStorage if available.
   * @returns The API client with headers set.
   */
  public static async getApiClient(): Promise<ApiClient> {
    if (!ApiClientManager.client) {
      ApiClientManager.client = await ApiClientManager.api.getClient<ApiClient>();
    }

    if (localStorage.getItem('token')) {
      ApiClientManager.client.defaults.headers['authorization'] =
        `Bearer ${localStorage.getItem('token')}`;
    }
    return ApiClientManager.client;
  }
}
