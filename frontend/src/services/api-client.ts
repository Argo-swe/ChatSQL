import { OpenAPIClientAxios } from 'openapi-client-axios';
import type { Client as ApiClient } from '../types/openapi.d.ts';

const api = new OpenAPIClientAxios({
    definition: import.meta.env.VITE_OPENAPI_BASE_URL
});

export const getApiClient = async () => {
  const client = await api.getClient<ApiClient>();

  if (localStorage.getItem("token")) {
    client.defaults.headers['authorization'] = `Bearer ${localStorage.getItem("token")}`;
  }

  return client;
}
