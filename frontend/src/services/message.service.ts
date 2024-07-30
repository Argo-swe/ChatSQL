import type { ToastMessageOptions } from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const defaultLifeTime = 5000;

export const messageService = () => {
  const toast = useToast();

  const messageInfo = (title: string, detail: string, lifeTime?: number) => {
    message({
      severity: 'info',
      summary: title,
      detail: detail,
      life: lifeTime ?? defaultLifeTime
    });
  };

  const messageSuccess = (title: string, detail: string, lifeTime?: number) => {
    message({
      severity: 'success',
      summary: title,
      detail: detail,
      life: lifeTime ?? defaultLifeTime
    });
  };

  const messageWarning = (title: string, detail: string, lifeTime?: number) => {
    message({
      severity: 'warn',
      summary: title,
      detail: detail,
      life: lifeTime ?? defaultLifeTime
    });
  };

  const messageError = (title: string, detail: string, lifeTime?: number) => {
    message({
      severity: 'error',
      summary: title,
      detail: detail,
      life: lifeTime ?? defaultLifeTime
    });
  };

  const message = (message: ToastMessageOptions) => {
    toast.add(message);
  };

  return {
    messageInfo,
    messageSuccess,
    messageWarning,
    messageError,
    message
  };
};
