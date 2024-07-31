export default class UtilsService {
  static downloadFile(fileName: string, data: any) {
    const downloadLink = document.createElement('a');
    downloadLink.download = fileName;
    downloadLink.href = window.URL.createObjectURL(new Blob([data]));
    document.body.appendChild(downloadLink);
    downloadLink.click();
  }

  static stringToSnakeCase(string: string) {
    return (
      string &&
      string
        .match(/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+/g)
        .map((s) => s.toLowerCase())
        .join('_')
    );
  }

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

  static capitalizeString(str: string) {
    const auxStr = (' ' + str).slice(1);
    return auxStr.charAt(0).toUpperCase() + auxStr.slice(1);
  }
}
