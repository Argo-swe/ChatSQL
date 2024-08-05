/**
 * Utility service class providing various helper methods for common operations.
 */
export default class UtilsService {
  /**
   * Download a file with the specified name and data.
   * @param fileName - The name of the file to be downloaded.
   * @param data - The data to be included in the file.
   */
  static downloadFile(fileName: string, data: any) {
    const downloadLink = document.createElement('a');
    downloadLink.download = fileName;
    downloadLink.href = window.URL.createObjectURL(new Blob([data]));
    document.body.appendChild(downloadLink);
    downloadLink.click();
  }

  /**
   * Converts a given string to snake_case.
   * @param string - The input string to be converted.
   * @returns The string converted to snake_case.
   */
  static stringToSnakeCase(string: string): string {
    //match(/[A-Z][A-Z]*(?=[A-Z][a-z]*\d*|\b)|[A-Z]?[a-z]+\d*|[A-Z]|\d+/g)
    const segments =
      string.match(/[A-Z]{2,}(?=[a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+/g) || [];

    return segments.map((s) => s.toLowerCase()).join('_');
  }

  /**
   * Adds capitalized keys to a given data object under the 'text' property.
   * @param data - The object to be updated.
   */
  static addCapitalizeValues(data: any) {
    const capitalizedText: { [id: string]: string } = {};

    if ('text' in data) {
      for (const key in data['text']) {
        capitalizedText[UtilsService.capitalizeString(key)] = `@.capitalize:text.${key}`;
      }
    }

    data.text = {
      ...data.text,
      ...capitalizedText
    };
    return data;
  }

  /**
   * Capitalizes the first letter of the given string.
   * @param str - The input string to be capitalized.
   * @returns The capitalized string.
   */
  static capitalizeString(str: string): string {
    const auxStr = (' ' + str).slice(1);
    return auxStr.charAt(0).toUpperCase() + auxStr.slice(1);
  }
}
