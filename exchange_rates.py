# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class Cash(ABC):
    def __init__(self, amount: float):
        """
        In base currency EUR
        Args:
            amount (float): Amount
        """
        self.amount = amount
    
    def get_rate( self, from_currency:str, to_currency:str ):
        return to_currency/from_currency

    