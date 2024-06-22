import { OpenAPIClientAxios } from 'openapi-client-axios';
import type { Client as ApiClient } from '../types/openapi.d.ts';

const api = new OpenAPIClientAxios({
    definition: import.meta.env.VITE_OPENAPI_BASE_URL
});

const client = await api.getClient<ApiClient>();


export const getApiClient = () => {
  return client;
}
