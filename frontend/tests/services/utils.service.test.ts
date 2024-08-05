import UtilsService from '../../src/services/utils.service';

describe('UtilsService', () => {
  test('stringToSnakeCase should convert string to snake case', () => {
    expect(UtilsService.stringToSnakeCase('TestString')).toBe('test_string');
    expect(UtilsService.stringToSnakeCase('anotherTestString')).toBe('another_test_string');
    expect(UtilsService.stringToSnakeCase('Test123String')).toBe('test123_string');
    expect(UtilsService.stringToSnakeCase('')).toBe('');
    expect(UtilsService.stringToSnakeCase(null)).toBe(null);
  });
});
