import json
from dataclasses import dataclass


@dataclass
class Bismillah:
    msg: str

    @staticmethod
    def create(msg: str):
        return "Bismillah!"
