# -*- coding: utf-8 -*-

from asset_portfolio import AssetPortfolio
from stock import Stock

class Program(object):
    
    def main( self ):
        
        ''' SEE README FOR INSTRUCTIONS '''
        
        self.test1()
        
        input('Done...(Press any key)')
        
    def test1( self ):
        
        portfolio = AssetPortfolio()        
        portfolio.add( Stock('ABC',200,4) )
        portfolio.add( Stock('DDW',100,10) )
        
        try:
        
            assert self.are_equal( portfolio.value(), 1800 )
        
        except AssertionError:
            print('Test 1 Failed, Expected Value:' + '\t' + '1800' + ',\t' + 'Actual Value: \t' + str(portfolio.value()) + '\n')
            
    def are_equal( self, d1:float, d2:float ):
        return abs(d1-d2) < 0.0001
    
if __name__ == '__main__':
    
    Program().main()