import UtilsService from '../../src/services/utils.service';

/**
 * Test suite for the UtilsService class.
 */
describe('UtilsService', () => {
  /**
   * Test suite for the downloadFile method.
   */
  describe('downloadFile', () => {
    // Hook that runs once before all tests
    beforeAll(() => {
      window.URL.createObjectURL = jest.fn();
    });

    // Hook that runs once after all tests
    afterAll(() => {
      jest.restoreAllMocks();
    });

    // Single and isolated test case
    it('should trigger a download', () => {
      const createElementSpy = jest.spyOn(document, 'createElement');
      const appendChildSpy = jest.spyOn(document.body, 'appendChild').mockImplementation((node) => {
        return node;
      });
      const clickSpy = jest.fn();

      createElementSpy.mockReturnValue({
        download: '',
        href: '',
        click: clickSpy
      } as unknown as HTMLAnchorElement);

      UtilsService.downloadFile('test.txt', 'File content');

      expect(createElementSpy).toHaveBeenCalledWith('a');
      expect(appendChildSpy).toHaveBeenCalled();
      expect(clickSpy).toHaveBeenCalled();
    });
  });

  /**
   * Test suite for the stringToSnakeCase method.
   */
  describe('stringToSnakeCase', () => {
    it('should convert string to snake_case', () => {
      expect(UtilsService.stringToSnakeCase('TestString')).toBe('test_string');
      expect(UtilsService.stringToSnakeCase('anotherTestString')).toBe('another_test_string');
      expect(UtilsService.stringToSnakeCase('Test123String')).toBe('test123_string');
      expect(UtilsService.stringToSnakeCase('123Test123String')).toBe('123_test123_string');
      expect(UtilsService.stringToSnakeCase('DDDddDDd')).toBe('dd_ddd_d_dd');
      expect(UtilsService.stringToSnakeCase('HTTPResponseCode2024')).toBe('http_response_code2024');
      expect(UtilsService.stringToSnakeCase('New test name')).toBe('new_test_name');
      expect(UtilsService.stringToSnakeCase('')).toBe('');
    });
  });

  /**
   * Test suite for the addCapitalizeValues method.
   */
  describe('addCapitalizeValues', () => {
    // Single and isolated test case
    it('should add capitalized keys', () => {
      const data = {
        text: {
          key1: 'value',
          key2: 'value'
        }
      };

      const result = UtilsService.addCapitalizeValues(data);

      expect(result).toEqual({
        text: {
          key1: 'value',
          key2: 'value',
          Key1: '@.capitalize:text.key1',
          Key2: '@.capitalize:text.key2'
        }
      });
    });
  });

  /**
   * Test suite for the capitalizeString method.
   */
  describe('capitalizeString', () => {
    // Single and isolated test case
    it('should capitalize the first letter of a string.', () => {
      expect(UtilsService.capitalizeString('string')).toBe('String');
      expect(UtilsService.capitalizeString('a')).toBe('A');
      expect(UtilsService.capitalizeString('aa')).toBe('Aa');
      expect(UtilsService.capitalizeString('String')).toBe('String');
    });
  });
});
