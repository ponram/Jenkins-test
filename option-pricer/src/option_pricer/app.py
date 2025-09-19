#!/usr/bin/env python3
"""
European Option Pricing using QuantLib
"""
import QuantLib as ql
from typing import Dict, Any

class OptionPricer:
    """European option pricer using Black-Scholes-Merton model"""
    
    def __init__(self, spot_price: float, strike_price: float, 
                 risk_free_rate: float, volatility: float, 
                 dividend_yield: float = 0.0):
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.dividend_yield = dividend_yield
        self.day_count = ql.Actual365Fixed()
        self.calendar = ql.TARGET()
    
    def price_european_option(self, maturity_date: str, 
                            option_type: str = "call") -> Dict[str, Any]:
        """Price European option using Black-Scholes-Merton formula"""
        
        # Set evaluation date to a fixed date for testing
        calculation_date = ql.Date().todaysDate()
        ql.Settings.instance().evaluationDate = calculation_date
        
        # Parse and validate maturity date
        maturity = ql.Date(maturity_date, "%Y-%m-%d")
        if not self.calendar.isBusinessDay(maturity):
            maturity = self.calendar.adjust(maturity)
        
        # Create option type
        opt_type = ql.Option.Call if option_type.lower() == "call" else ql.Option.Put
        
        # Create payoff and exercise
        payoff = ql.PlainVanillaPayoff(opt_type, self.strike_price)
        exercise = ql.EuropeanExercise(maturity)
        
        # Create option
        option = ql.VanillaOption(payoff, exercise)
        
        # Market data
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(self.spot_price))
        risk_free_curve = ql.YieldTermStructureHandle(
            ql.FlatForward(calculation_date, self.risk_free_rate, self.day_count)
        )
        dividend_curve = ql.YieldTermStructureHandle(
            ql.FlatForward(calculation_date, self.dividend_yield, self.day_count)
        )
        volatility_curve = ql.BlackVolTermStructureHandle(
            ql.BlackConstantVol(calculation_date, self.calendar, 
                              self.volatility, self.day_count)
        )
        
        # Create Black-Scholes process
        bsm_process = ql.BlackScholesMertonProcess(
            spot_handle, dividend_curve, risk_free_curve, volatility_curve
        )
        
        # Set pricing engine
        engine = ql.AnalyticEuropeanEngine(bsm_process)
        option.setPricingEngine(engine)
        
        # Calculate Greeks
        return {
            "price": option.NPV(),
            "delta": option.delta(),
            "gamma": option.gamma(),
            "theta": option.theta(),
            "vega": option.vega(),
            "rho": option.rho()
        }

def main():
    """Example usage"""
    pricer = OptionPricer(
        spot_price=127.62,
        strike_price=130.0,
        risk_free_rate=0.001,
        volatility=0.20,
        dividend_yield=0.0163
    )
    
    result = pricer.price_european_option("2024-12-15", "call")
    print(f"Option Price: ${result['price']:.4f}")
    print(f"Delta: {result['delta']:.4f}")
    print(f"Gamma: {result['gamma']:.4f}")
    
    return result

if __name__ == "__main__":
    main()
