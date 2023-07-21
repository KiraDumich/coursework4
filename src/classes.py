from abc import ABC
import json
import requests


class API(ABC):
    def __init__(self, key):
        self.key = key
        self.vacansies = []




