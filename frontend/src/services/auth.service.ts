import { jwtDecode, type JwtPayload } from 'jwt-decode';

/**
 * AuthService class provides authentication-related functionalities.
 */
export default class AuthService {
  // Key for token in localStorage
  static readonly LS_TOKEN_KEY = 'token';

  /**
   * Removes the token from localStorage and sends a custom event to notify the change.
   */
  static logout() {
    localStorage.removeItem(AuthService.LS_TOKEN_KEY);
    window.dispatchEvent(new CustomEvent('token-localstorage-changed'));
  }

  /**
   * Check if the token is in localStorage and has not expired.
   */
  static isLogged(): boolean {
    const token = localStorage.getItem(AuthService.LS_TOKEN_KEY);

    if (!token) {
      return false;
    }

    return AuthService.checkJwtExpiration(token);
  }

  /**
   * Decode the JWT token and check its expiration date.
   * @param token - The JWT token to verify.
   */
  private static checkJwtExpiration(token: string): boolean {
    const decoded = jwtDecode<JwtPayload>(token);

    return !AuthService.isTokenExpired(decoded.exp);
  }

  /**
   * Performs expiration date verification.
   * @param exp - The token expiration date in seconds.
   */
  private static isTokenExpired(exp?: number): boolean {
    const actualTime: number = new Date().getTime();

    if (exp) {
      return 1000 * exp - actualTime < 5000;
    }
    return true;
  }
}
