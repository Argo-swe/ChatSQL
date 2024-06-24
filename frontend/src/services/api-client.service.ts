import { OpenAPIClientAxios } from 'openapi-client-axios';
import type { Client as ApiClient } from '../types/openapi';

const api = new OpenAPIClientAxios({
    definition: import.meta.env.VITE_OPENAPI_BASE_URL
});

const client = await api.getClient<ApiClient>();

export const getApiClient = () => {
  if (localStorage.getItem("token")) {
    client.defaults.headers['authorization'] = `Bearer ${localStorage.getItem("token")}`;
  }
  return client;
}
