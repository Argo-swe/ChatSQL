import type { ToastMessageOptions } from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const defaultLifeTime = 5000;

/**
 * Provides a set of functions to display different types of toast messages.
 */
export const messageService = () => {
  const toast = useToast();

  /**
   * Displays an informational message with optional lifetime.
   *
   * @param title - The title or summary of the message.
   * @param detail - Description of the message.
   * @param lifeTime - (Optional) The duration in milliseconds for which the message will be displayed.
   */
  const messageInfo = (title: string, detail: string, lifeTime?: number) => {
    message({
      severity: 'info',
      summary: title,
      detail: detail,
      life: lifeTime ?? defaultLifeTime
    });
  };

  /**
   * Displays a success message with optional lifetime.
   *
   * @param title - The title or summary of the message.
   * @param detail - Description of the message.
   * @param lifeTime - (Optional) The duration in milliseconds for which the message will be displayed.
   */
  const messageSuccess = (title: string, detail: string, lifeTime?: number) => {
    message({
      severity: 'success',
      summary: title,
      detail: detail,
      life: lifeTime ?? defaultLifeTime
    });
  };

  /**
   * Displays a warning message with optional lifetime.
   *
   * @param title - The title or summary of the message.
   * @param detail - Description of the message.
   * @param lifeTime - (Optional) The duration in milliseconds for which the message will be displayed.
   */
  const messageWarning = (title: string, detail: string, lifeTime?: number) => {
    message({
      severity: 'warn',
      summary: title,
      detail: detail,
      life: lifeTime ?? defaultLifeTime
    });
  };

  /**
   * Displays an error message with optional lifetime.
   *
   * @param title - The title or summary of the message.
   * @param detail - Description of the message.
   * @param lifeTime - (Optional) The duration in milliseconds for which the message will be displayed.
   */
  const messageError = (title: string, detail: string, lifeTime?: number) => {
    message({
      severity: 'error',
      summary: title,
      detail: detail,
      life: lifeTime ?? defaultLifeTime
    });
  };

  /**
   * Adds a message to the toast display.
   */
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
