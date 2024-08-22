import type { ToastMessageOptions } from 'primevue/toast';
import type { ToastServiceMethods } from 'primevue/toastservice';
import { useToast } from 'primevue/usetoast';

/**
 * MessageService class provides a set of methods to display different types of toast messages.
 */
export default class MessageService {
  private toast: ToastServiceMethods;
  private readonly defaultLifeTime: number = 5000;

  /**
   * Private constructor to prevent direct instantiation.
   */
  private constructor() {
    this.toast = useToast();
  }

  /**
   * Displays an informational message with optional lifetime.
   * @param title - The title or summary of the message.
   * @param detail - Description of the message.
   * @param lifeTime - (Optional) The duration in milliseconds for which the message will be displayed.
   */
  public messageInfo(title: string, detail: string, lifeTime?: number) {
    this.message({
      severity: 'info',
      summary: title,
      detail: detail,
      life: lifeTime ?? this.defaultLifeTime
    });
  }

  /**
   * Displays a success message with optional lifetime.
   * @param title - The title or summary of the message.
   * @param detail - Description of the message.
   * @param lifeTime - (Optional) The duration in milliseconds for which the message will be displayed.
   */
  public messageSuccess(title: string, detail: string, lifeTime?: number) {
    this.message({
      severity: 'success',
      summary: title,
      detail: detail,
      life: lifeTime ?? this.defaultLifeTime
    });
  }

  /**
   * Displays a warning message with optional lifetime.
   * @param title - The title or summary of the message.
   * @param detail - Description of the message.
   * @param lifeTime - (Optional) The duration in milliseconds for which the message will be displayed.
   */
  public messageWarning(title: string, detail: string, lifeTime?: number) {
    this.message({
      severity: 'warn',
      summary: title,
      detail: detail,
      life: lifeTime ?? this.defaultLifeTime
    });
  }

  /**
   * Displays an error message with optional lifetime.
   * @param title - The title or summary of the message.
   * @param detail - Description of the message.
   * @param lifeTime - (Optional) The duration in milliseconds for which the message will be displayed.
   */
  public messageError(title: string, detail: string, lifeTime?: number) {
    this.message({
      severity: 'error',
      summary: title,
      detail: detail,
      life: lifeTime ?? this.defaultLifeTime
    });
  }

  /**
   * Adds a message to the toast display.
   * @param message - The message configuration options.
   */
  private message(message: ToastMessageOptions) {
    this.toast.add(message);
  }

  /**
   * Factory method to get a configured instance of MessageService.
   * @returns An instance of MessageService.
   */
  public static getInstance(): MessageService {
    const instance = new MessageService();
    return instance;
  }
}
