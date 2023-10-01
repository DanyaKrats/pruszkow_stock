import logging

import jwt
from typing import Any, no_type_check, Optional
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import os
logger = logging.getLogger(__name__)

class Keys:
    def __init__(self) -> None:
        self.public_key, self.private_key = self.load_or_generate_rsa_keys()

    def load_or_generate_rsa_keys(self, private_key_file="rsa_priv.txt", public_key_file="rsa_pub.txt"):
        if os.path.exists(private_key_file) and os.path.exists(public_key_file):
            private_key, public_key = self.load_rsa_keys(private_key_file, public_key_file)
            return private_key, public_key
        else:
            self.generate_and_save_rsa_keys(private_key_file, public_key_file)
            return self.load_rsa_keys(private_key_file, public_key_file)


    def generate_and_save_rsa_keys(self, private_key_file="rsa_priv.txt", public_key_file="rsa_pub.txt"):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        with open(private_key_file, "wb") as private_key_file:
            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            private_key_file.write(private_key_pem)
        
        public_key = private_key.public_key()
        with open(public_key_file, "wb") as public_key_file:
            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            public_key_file.write(public_key_pem)


    def load_rsa_keys(self, private_key_file="rsa_priv.txt", public_key_file="rsa_pub.txt"):
        with open(private_key_file, "rb") as private_key_file:
            private_key_pem = private_key_file.read()
            private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        
        with open(public_key_file, "rb") as public_key_file:
            public_key_pem = public_key_file.read()
            public_key = serialization.load_pem_public_key(public_key_pem)
        
        return private_key, public_key



class JWTService:
    def __init__(self) -> None:
        self.algorithm = "RS256"
        self.algorithms = ["RS256"]
        self.keys:Keys = Keys()
    
    def check_rsa_keys(self): 
        if not self.keys:
            self.keys = 123 
            if self.keys is None:
                raise ValueError("Keys don't exist or Docker is not running")

    async def encode_jwt(self, payload: dict[str, Any] = {}, secret: None = None) -> str:
        self.check_rsa_keys()
        token = jwt.encode(
            payload=payload, key=self.keys.private_key, algorithm=self.algorithm
        )

        logger.info(f"Created token.")

        return token

    async def decode_token(self, token: str, audience: str =None ,**kwargs: Any) -> dict[str, Any]:
        self.check_rsa_keys()
        token = token.replace("Bearer ", "")
        if audience:
            decoded = jwt.decode(
                token,
                key=self.keys().public_key,
                algorithms=self.algorithms,
                audience=audience,
                **kwargs,
            )
            return decoded
        decoded = jwt.decode(
            token,
            key=self.keys().public_key,
            algorithms=self.algorithms,
            **kwargs,
        )
        return decoded

    async def verify_token(self, token: str, aud:str=None) -> bool:
        self.check_rsa_keys()
        try:
            if aud:
                await self.decode_token(token=token, audience=aud)
            else:
                await self.decode_token(token)
            return True
        except:
            return False
        
    async def get_module(self) -> int:
        self.check_rsa_keys()
        return self.keys().n

    async def get_pub_key_expanent(self) -> int:
        self.check_rsa_keys()
        return self.keys().e


