# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class Cash(ABC):
    def __init__(self, amount: float, code: str):
        """
        In base currency EUR
        Args:
            amount (float): Amount
        """
        self.amount = amount
        self.code = code
        
    
    def get_rate( self, from_currency:str, to_currency:str ):
        return to_currency/from_currency

    