import { jwtDecode, type JwtPayload } from "jwt-decode";

export default class AuthService {
    static LS_TOKEN_KEY = 'token';

    static logout() {
        localStorage.removeItem(AuthService.LS_TOKEN_KEY);
        window.dispatchEvent(new CustomEvent('token-localstorage-changed'));
    }

    static isLogged(): boolean {
        const token = localStorage.getItem(AuthService.LS_TOKEN_KEY);

        if (!token) {
            return false;
        }

        return AuthService.checkJwtExpiration(token);
    }

    private static checkJwtExpiration(token: string): boolean {
        const decoded = jwtDecode<JwtPayload>(token);

        return !AuthService.isTokenExpired(decoded.exp);
    }

    private static isTokenExpired(exp: number | undefined): boolean {
        const actualTime: number = (new Date()).getTime();

        if (exp) {
          return ((1000 * exp) - actualTime) < 5000;
        }
        return true;
    }
}
