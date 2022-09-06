#!/usr/bin/env python3

from configparser import ConfigParser
import os
import jwt

host: str = "127.0.0.1"


def set_up():
    """
    Set up the environment for the site.
    """

    env = os.getenv("ENV", ".config")

    if env == ".config":
        config = ConfigParser()
        config.read(".config")
        config = config["AUTH0"]

    else:
        config = {
            "DOMAIN": os.getenv(f"DOMAIN", f"{host}"),
            "API_AUDIENCE": os.getenv("API_AUDIENCE", f"{host}/private"),
            "ISSUER": os.getenv("ISSUER", f"{host}"),
            "ALGORITHMS": os.getenv("ALGORITHMS", "RS256"),
        }

    return config


class VerifyToken:
    """
    Verify the token using PyJWT.
    """

    def __init__(self, token):
        self.token = token
        self.config = set_up()

        jwks_url = f"https://{self.config['DOMAIN']}/.well-known/jwks.json"

        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        """
        Verify the token.
        """

        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return payload
