# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class IExchangeRates(ABC):
    
    @abstractmethod
    def get_rate( self, from_currency:str, to_currency:str ):
        pass