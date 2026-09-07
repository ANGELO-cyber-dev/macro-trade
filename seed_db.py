from database import SessionLocal
from models import Instrument, MacroIndicator, AssetClass

def seed_data():
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(Instrument).first():
        print("Database already seeded.")
        db.close()
        return

    # Seed Instruments
    instruments = [
        # FX
        Instrument(ticker="EUR/USD", name="Euro / US Dollar", asset_class=AssetClass.FX, base_currency="EUR", quote_currency="USD"),
        Instrument(ticker="GBP/USD", name="British Pound / US Dollar", asset_class=AssetClass.FX, base_currency="GBP", quote_currency="USD"),
        Instrument(ticker="USD/JPY", name="US Dollar / Japanese Yen", asset_class=AssetClass.FX, base_currency="USD", quote_currency="JPY"),
        Instrument(ticker="AUD/USD", name="Australian Dollar / US Dollar", asset_class=AssetClass.FX, base_currency="AUD", quote_currency="USD"),
        Instrument(ticker="USD/CAD", name="US Dollar / Canadian Dollar", asset_class=AssetClass.FX, base_currency="USD", quote_currency="CAD"),
        Instrument(ticker="USD/CHF", name="US Dollar / Swiss Franc", asset_class=AssetClass.FX, base_currency="USD", quote_currency="CHF"),
        Instrument(ticker="NZD/USD", name="New Zealand Dollar / US Dollar", asset_class=AssetClass.FX, base_currency="NZD", quote_currency="USD"),
        
        # Commodities
        Instrument(ticker="GOLD", name="Gold Spot", asset_class=AssetClass.COMMODITIES, base_currency="XAU", quote_currency="USD"),
        Instrument(ticker="SILVER", name="Silver Spot", asset_class=AssetClass.COMMODITIES, base_currency="XAG", quote_currency="USD"),
        Instrument(ticker="OIL", name="Crude Oil WTI", asset_class=AssetClass.COMMODITIES, base_currency="WTI", quote_currency="USD"),
        Instrument(ticker="COPPER", name="Copper Futures", asset_class=AssetClass.COMMODITIES, base_currency="HG", quote_currency="USD"),

        # Crypto
        Instrument(ticker="BTC", name="Bitcoin", asset_class=AssetClass.CRYPTO, base_currency="BTC", quote_currency="USD"),
        Instrument(ticker="ETH", name="Ethereum", asset_class=AssetClass.CRYPTO, base_currency="ETH", quote_currency="USD"),
        Instrument(ticker="SOL", name="Solana", asset_class=AssetClass.CRYPTO, base_currency="SOL", quote_currency="USD"),

        # Indices
        Instrument(ticker="SPX", name="S&P 500", asset_class=AssetClass.INDICES),
        Instrument(ticker="NDX", name="Nasdaq 100", asset_class=AssetClass.INDICES),
        Instrument(ticker="DAX", name="DAX Germany", asset_class=AssetClass.INDICES),
        Instrument(ticker="FTSE", name="FTSE 100", asset_class=AssetClass.INDICES),
        Instrument(ticker="N225", name="Nikkei 225", asset_class=AssetClass.INDICES),

        # Rates
        Instrument(ticker="US_2Y", name="US 2-Year Treasury Yield", asset_class=AssetClass.RATES),
        Instrument(ticker="US_10Y", name="US 10-Year Treasury Yield", asset_class=AssetClass.RATES),
        Instrument(ticker="DE_10Y", name="Germany 10-Year Bund Yield", asset_class=AssetClass.RATES),
        Instrument(ticker="UK_10Y", name="UK 10-Year Gilt Yield", asset_class=AssetClass.RATES),
        Instrument(ticker="JP_10Y", name="Japan 10-Year Government Bond Yield", asset_class=AssetClass.RATES)
    ]

    # Seed Macro Indicators
    macro_indicators = [
        MacroIndicator(series_id="CPIAUCSL", name="Consumer Price Index (CPI)", category="Inflation", frequency="Monthly"),
        MacroIndicator(series_id="PCEPI", name="Personal Consumption Expenditures (PCE)", category="Inflation", frequency="Monthly"),
        MacroIndicator(series_id="PAYEMS", name="Nonfarm Payrolls (NFP)", category="Labor", frequency="Monthly"),
        MacroIndicator(series_id="UNRATE", name="Unemployment Rate", category="Labor", frequency="Monthly"),
        MacroIndicator(series_id="GDP", name="Gross Domestic Product", category="Growth", frequency="Quarterly"),
        MacroIndicator(series_id="M2SL", name="M2 Money Supply", category="Liquidity", frequency="Monthly")
    ]

    db.add_all(instruments)
    db.add_all(macro_indicators)
    db.commit()
    db.close()
    print("Core universe and macro indicators successfully seeded!")

if __name__ == "__main__":
    seed_data()
