import { jwtDecode } from 'jwt-decode';
import AuthService from '../../src/services/auth.service';

// Mock of the jwt-decode module
jest.mock('jwt-decode');

/**
 * Test suite for the AuthService class.
 */
describe('AuthService', () => {
  // Hook that runs before each test
  beforeEach(() => {
    localStorage.clear();
  });

  // Hook that runs once after all tests
  afterAll(() => {
    jest.restoreAllMocks();
  });

  /**
   * Test suite for the logout method.
   */
  describe('logout', () => {
    // Single and isolated test case
    it('should remove token from localStorage and dispatch event', () => {
      const dispatchEventSpy = jest.spyOn(window, 'dispatchEvent');
      localStorage.setItem(AuthService.LS_TOKEN_KEY, 'accesToken');
      AuthService.logout();
      expect(localStorage.getItem(AuthService.LS_TOKEN_KEY)).toBeNull();
      expect(dispatchEventSpy).toHaveBeenCalledWith(new CustomEvent('token-localstorage-changed'));
    });
  });

  /**
   * Test suite for the isLogged method.
   */
  describe('isLogged', () => {
    // Single and isolated test case
    it('should return false if no token is found', () => {
      expect(AuthService.isLogged()).toBe(false);
    });

    // Single and isolated test case
    it('should return false if the token is expired', () => {
      (jwtDecode as jest.Mock).mockReturnValue({ exp: Math.floor(Date.now() / 1000) - 1000 });
      localStorage.setItem(AuthService.LS_TOKEN_KEY, 'expiredToken');
      expect(AuthService.isLogged()).toBe(false);
    });

    // Single and isolated test case
    it('should return true if the token is valid', () => {
      (jwtDecode as jest.Mock).mockReturnValue({ exp: Math.floor(Date.now() / 1000) + 1000 });
      localStorage.setItem(AuthService.LS_TOKEN_KEY, 'validToken');
      expect(AuthService.isLogged()).toBe(true);
    });

    // Single and isolated test case
    it('should return false if expiration date is undefined', () => {
      (jwtDecode as jest.Mock).mockReturnValue({});
      localStorage.setItem(AuthService.LS_TOKEN_KEY, 'accessToken');
      expect(AuthService.isLogged()).toBe(false);
    });
  });
});
