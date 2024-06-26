export const downloadFile = (fileName: string, data: any) => {
  const downloadLink = document.createElement('a');
  downloadLink.download = fileName;
  downloadLink.href = window.URL.createObjectURL(new Blob([data]));
  document.body.appendChild(downloadLink);
  downloadLink.click();
}

export const stringToSnakeCase = (string: string) => {
  return string && string.match(/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+/g)
      .map(s => s.toLowerCase())
      .join('_');
}
