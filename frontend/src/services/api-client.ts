import { OpenAPIClientAxios } from 'openapi-client-axios';
import type { Client as ApiClient } from '../types/openapi.d.ts';

const api = new OpenAPIClientAxios({
    definition: import.meta.env.VITE_OPENAPI_BASE_URL
});

export const getApiClient = async () => {
  const client = await api.getClient<ApiClient>();

//   // add auth token
//   client.default.headers['authorization'] = `Bearer ${API_TOKEN}`;

  return client;
}
