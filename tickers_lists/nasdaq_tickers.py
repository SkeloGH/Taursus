"""List of tickers from NASDAQ."""
tickers = [
    # S&P 500 tickers:
    "A", # Agilent Technologies, Inc.
    "AAPL", # Apple Inc.
    "ABBV", # AbbVie Inc.
    "ABNB", # Airbnb, Inc.
    "ABT", # Abbott Laboratories
    "ACGL", # Arch Capital Group Ltd.
    "ACN", # Accenture plc
    "ADBE", # Adobe Inc.
    "ADI", # Analog Devices, Inc.
    "ADM", # Archer-Daniels-Midland Company
    "ADP", # Automatic Data Processing, Inc.
    "ADSK", # Autodesk, Inc.
    "AEE", # Ameren Corporation
    "AEP", # American Electric Power Company, Inc.
    "AES", # The AES Corporation
    "AFL", # Aflac Incorporated
    "AIG", # American International Group, Inc.
    "AIZ", # Assurant, Inc.
    "AJG", # Arthur J. Gallagher & Co.
    "AKAM", # Akamai Technologies, Inc.
    "ALB", # Albemarle Corporation
    "ALGN", # Align Technology, Inc.
    "ALL", # The Allstate Corporation
    "ALLE", # Allegion plc
    "AMAT", # Applied Materials, Inc.
    "AMCR", # Amcor plc
    "AMD", # Advanced Micro Devices, Inc.
    "AME", # AMETEK, Inc.
    "AMGN", # Amgen Inc.
    "AMP", # Ameriprise Financial, Inc.
    "AMT", # American Tower Corporation
    "AMZN", # Amazon.com, Inc.
    "ANET", # Arista Networks, Inc.
    "ANSS", # ANSYS, Inc.
    "AON", # Aon plc
    "AOS", # A. O. Smith Corporation
    "APA", # APA Corporation
    "APD", # Air Products and Chemicals, Inc.
    "APH", # Amphenol Corporation
    "APTV", # Aptiv PLC
    "ARE", # Alexandria Real Estate Equities, Inc.
    "ATO", # Atmos Energy Corporation
    "AVB", # AvalonBay Communities, Inc.
    "AVGO", # Broadcom Inc.
    "AVY", # Avery Dennison Corporation
    "AWK", # American Water Works Company, Inc.
    "AXON", # Axon Enterprise, Inc.
    "AXP", # American Express Company
    "AZO", # AutoZone, Inc.
    "BA", # The Boeing Company
    "BAC", # Bank of America Corporation
    "BALL", # Ball Corporation
    "BAX", # Baxter International Inc.
    "BBWI", # Bath & Body Works, Inc.
    "BBY", # Best Buy Co., Inc.
    "BDX", # Becton, Dickinson and Company
    "BEN", # Franklin Resources, Inc.
    "BF-A",  # Brown-Forman Corporation
    "BF-B",  # Brown-Forman Corporation
    "BG", # Bunge Global SA
    "BIIB", # Biogen Inc.
    "BK", # The Bank of New York Mellon Corporation
    "BKNG", # Booking Holdings Inc.
    "BKR", # Baker Hughes Company
    "BLDR", # Builders FirstSource, Inc.
    "BLK", # BlackRock, Inc.
    "BMY", # Bristol-Myers Squibb Company
    "BR", # Broadridge Financial Solutions, Inc.
    "BRK-A", # Berkshire Hathaway Inc.
    "BRK-B", # Berkshire Hathaway Inc.
    "BRO", # Brown & Brown, Inc.
    "BSX", # Boston Scientific Corporation
    "BWA", # BorgWarner Inc.
    "BX", # Blackstone Inc.
    "BXP", # BXP, Inc.
    "C", # Citigroup Inc.
    "CAG", # Conagra Brands, Inc.
    "CAH", # Cardinal Health, Inc.
    "CARR", # Carrier Global Corporation
    "CAT", # Caterpillar Inc.
    "CB", # Chubb Limited
    "CBOE", # Cboe Global Markets, Inc.
    "CBRE", # CBRE Group, Inc.
    "CCI", # Crown Castle Inc.
    "CCL", # Carnival Corporation & plc
    "CDNS", # Cadence Design Systems, Inc.
    "CDW", # CDW Corporation
    "CE", # Celanese Corporation
    "CEG", # Constellation Energy Corporation
    "CF", # CF Industries Holdings, Inc.
    "CFG", # Citizens Financial Group, Inc.
    "CHD", # Church & Dwight Co., Inc.
    "CHRW", # C.H. Robinson Worldwide, Inc.
    "CHTR", # Charter Communications, Inc.
    "CI", # The Cigna Group
    "CINF", # Cincinnati Financial Corporation
    "CL", # Colgate-Palmolive Company
    "CLX", # The Clorox Company
    "CMCSA", # Comcast Corporation
    "CME", # CME Group Inc.
    "CMG", # Chipotle Mexican Grill, Inc.
    "CMI", # Cummins Inc.
    "CMS", # CMS Energy Corporation
    "CNC", # Centene Corporation
    "CNP", # CenterPoint Energy, Inc.
    "COF", # Capital One Financial Corporation
    "COO", # The Cooper Companies, Inc.
    "COP", # ConocoPhillips
    "COR", # Cencora, Inc.
    "COST", # Costco Wholesale Corporation
    "CPAY", # Corpay, Inc.
    "CPB", # Campbell Soup Company
    "CPRT", # Copart, Inc.
    "CPT", # Camden Property Trust
    "CRL", # Charles River Laboratories International, Inc.
    "CRM", # Salesforce, Inc.
    "CRWD", # CrowdStrike Holdings, Inc.
    "CSCO", # Cisco Systems, Inc.
    "CSGP", # CoStar Group, Inc.
    "CSX", # CSX Corporation
    "CTAS", # Cintas Corporation
    "CTLT", # Catalent, Inc.
    "CTRA", # Coterra Energy Inc.
    "CTSH", # Cognizant Technology Solutions Corporation
    "CTVA", # Corteva, Inc.
    "CVS", # CVS Health Corporation
    "CVX", # Chevron Corporation
    "CZR", # Caesars Entertainment, Inc.
    "D", # Dominion Energy, Inc.
    "DAL", # Delta Air Lines, Inc.
    "DAY", # Dayforce Inc.
    "DD", # DuPont de Nemours, Inc.
    "DE", # Deere & Company
    "DECK", # Deckers Outdoor Corporation
    "DELL", # Dell Technologies Inc.
    "DFS", # Discover Financial Services
    "DG", # Dollar General Corporation
    "DGX", # Quest Diagnostics Incorporated
    "DHI", # D.R. Horton, Inc.
    "DHR", # Danaher Corporation
    "DIS", # The Walt Disney Company
    "DLR", # Digital Realty Trust, Inc.
    "DLTR", # Dollar Tree, Inc.
    "DOC", # Healthpeak Properties, Inc.
    "DOV", # Dover Corporation
    "DOW", # Dow Inc.
    "DPZ", # Domino's Pizza, Inc.
    "DRI", # Darden Restaurants, Inc.
    "DTE", # DTE Energy Company
    "DUK", # Duke Energy Corporation
    "DVA", # DaVita Inc.
    "DVN", # Devon Energy Corporation
    "DXCM", # DexCom, Inc.
    "EA", # Electronic Arts Inc.
    "EBAY", # eBay Inc.
    "ECL", # Ecolab Inc.
    "ED", # Consolidated Edison, Inc.
    "EFX", # Equifax Inc.
    "EG", # Everest Group, Ltd.
    "EIX", # Edison International
    "EL", # The Estée Lauder Companies Inc.
    "ELV", # Elevance Health, Inc.
    "EMN", # Eastman Chemical Company
    "EMR", # Emerson Electric Co.
    "ENPH", # Enphase Energy, Inc.
    "EOG", # EOG Resources, Inc.
    "EPAM", # EPAM Systems, Inc.
    "EQIX", # Equinix, Inc.
    "EQR", # Equity Residential
    "EQT", # EQT Corporation
    "ERIE", # Erie Indemnity Company
    "ES", # Eversource Energy
    "ESS", # Essex Property Trust, Inc.
    "ETN", # Eaton Corporation plc
    "ETR", # Entergy Corporation
    "EVRG", # Evergy, Inc.
    "EW", # Edwards Lifesciences Corporation
    "EXC", # Exelon Corporation
    "EXPD", # Expeditors International of Washington, Inc.
    "EXPE", # Expedia Group, Inc.
    "EXR", # Extra Space Storage Inc.
    "F", # Ford Motor Company
    "FANG", # Diamondback Energy, Inc.
    "FAST", # Fastenal Company
    "FCX", # Freeport-McMoRan Inc.
    "FDS", # FactSet Research Systems Inc.
    "FDX", # FedEx Corporation
    "FE", # FirstEnergy Corp.
    "FFIV", # F5, Inc.
    "FI", # Fiserv, Inc.
    "FICO", # Fair Isaac Corporation
    "FIS", # Fidelity National Information Services, Inc.
    "FITB", # Fifth Third Bancorp
    "FMC", # FMC Corporation
    "FOX", # Fox Corporation
    "FOXA", # Fox Corporation
    "FRT", # Federal Realty Investment Trust
    "FSLR", # First Solar, Inc.
    "FTNT", # Fortinet, Inc.
    "FTV", # Fortive Corporation
    "GD", # General Dynamics Corporation
    "GDDY", # GoDaddy Inc.
    "GE", # General Electric Company
    "GEHC", # GE HealthCare Technologies Inc.
    "GEN", # Gen Digital Inc.
    "GEV", # GE Vernova Inc.
    "GILD", # Gilead Sciences, Inc.
    "GIS", # General Mills, Inc.
    "GL", # Globe Life Inc.
    "GLW", # Corning Incorporated
    "GM", # General Motors Company
    "GNRC", # Generac Holdings Inc.
    "GOOG", # Alphabet Inc.
    "GOOGL", # Alphabet Inc.
    "GPC", # Genuine Parts Company
    "GPN", # Global Payments Inc.
    "GRMN", # Garmin Ltd.
    "GS", # The Goldman Sachs Group, Inc.
    "GWW", # W.W. Grainger, Inc.
    "HAL", # Halliburton Company
    "HAS", # Hasbro, Inc.
    "HBAN", # Huntington Bancshares Incorporated
    "HCA", # HCA Healthcare, Inc.
    "HD", # The Home Depot, Inc.
    "HES", # Hess Corporation
    "HIG", # The Hartford Financial Services Group, Inc.
    "HII", # Huntington Ingalls Industries, Inc.
    "HLT", # Hilton Worldwide Holdings Inc.
    "HOLX", # Hologic, Inc.
    "HON", # Honeywell International Inc.
    "HPE", # Hewlett Packard Enterprise Company
    "HPQ", # HP Inc.
    "HRL", # Hormel Foods Corporation
    "HSIC", # Henry Schein, Inc.
    "HST", # Host Hotels & Resorts, Inc.
    "HSY", # The Hershey Company
    "HUBB", # Hubbell Incorporated
    "HUM", # Humana Inc.
    "HWM", # Howmet Aerospace Inc.
    "IBM", # International Business Machines Corporation
    "ICE", # Intercontinental Exchange, Inc.
    "IDXX", # IDEXX Laboratories, Inc.
    "IEX", # IDEX Corporation
    "IFF", # International Flavors & Fragrances Inc.
    "INCY", # Incyte Corporation
    "INTC", # Intel Corporation
    "INTU", # Intuit Inc.
    "INVH", # Invitation Homes Inc.
    "IP", # International Paper Company
    "IPG", # The Interpublic Group of Companies, Inc.
    "IQV", # IQVIA Holdings Inc.
    "IR", # Ingersoll Rand Inc.
    "IRM", # Iron Mountain Incorporated
    "ISRG", # Intuitive Surgical, Inc.
    "IT", # Gartner, Inc.
    "ITW", # Illinois Tool Works Inc.
    "IVZ", # Invesco Ltd.
    "J", # Jacobs Solutions Inc.
    "JBHT", # J.B. Hunt Transport Services, Inc.
    "JBL", # Jabil Inc.
    "JCI", # Johnson Controls International plc
    "JKHY", # Jack Henry & Associates, Inc.
    "JNJ", # Johnson & Johnson
    "JNPR", # Juniper Networks, Inc.
    "JPM", # JPMorgan Chase & Co.
    "K", # Kellanova
    "KDP", # Keurig Dr Pepper Inc.
    "KEY", # KeyCorp
    "KEYS", # Keysight Technologies, Inc.
    "KHC", # The Kraft Heinz Company
    "KIM", # Kimco Realty Corporation
    "KKR", # KKR & Co. Inc.
    "KLAC", # KLA Corporation
    "KMB", # Kimberly-Clark Corporation
    "KMI", # Kinder Morgan, Inc.
    "KMX", # CarMax, Inc.
    "KO", # The Coca-Cola Company
    "KR", # The Kroger Co.
    "KVUE", # Kenvue Inc.
    "L", # Loews Corporation
    "LDOS", # Leidos Holdings, Inc.
    "LEN", # Lennar Corporation
    "LH", # Labcorp Holdings Inc.
    "LHX", # L3Harris Technologies, Inc.
    "LIN", # Linde plc
    "LKQ", # LKQ Corporation
    "LLY", # Eli Lilly and Company
    "LMT", # Lockheed Martin Corporation
    "LNT", # Alliant Energy Corporation
    "LOW", # Lowe's Companies, Inc.
    "LRCX", # Lam Research Corporation
    "LULU", # Lululemon Athletica Inc.
    "LUV", # Southwest Airlines Co.
    "LVS", # Las Vegas Sands Corp.
    "LW", # Lamb Weston Holdings, Inc.
    "LYB", # LyondellBasell Industries N.V.
    "LYV", # Live Nation Entertainment, Inc.
    "MA", # Mastercard Incorporated
    "MAA", # Mid-America Apartment Communities, Inc.
    "MAR", # Marriott International, Inc.
    "MAS", # Masco Corporation
    "MCD", # McDonald's Corporation
    "MCHP", # Microchip Technology Incorporated
    "MCK", # McKesson Corporation
    "MCO", # Moody's Corporation
    "MDLZ", # Mondelez International, Inc.
    "MDT", # Medtronic plc
    "MET", # MetLife, Inc.
    "META", # Meta Platforms, Inc.
    "MGM", # MGM Resorts International
    "MHK", # Mohawk Industries, Inc.
    "MKC", # McCormick & Company, Incorporated
    "MKTX", # MarketAxess Holdings Inc.
    "MLM", # Martin Marietta Materials, Inc.
    "MMC", # Marsh & McLennan Companies, Inc.
    "MMM", # 3M Company
    "MNST", # Monster Beverage Corporation
    "MO", # Altria Group, Inc.
    "MOH", # Molina Healthcare, Inc.
    "MOS", # The Mosaic Company
    "MPC", # Marathon Petroleum Corporation
    "MPWR", # Monolithic Power Systems, Inc.
    "MRK", # Merck & Co., Inc.
    "MRNA", # Moderna, Inc.
    "MRO", # Marathon Oil Corporation
    "MS", # Morgan Stanley
    "MSCI", # MSCI Inc.
    "MSFT", # Microsoft Corporation
    "MSI", # Motorola Solutions, Inc.
    "MTB", # M&T Bank Corporation
    "MTCH", # Match Group, Inc.
    "MTD", # Mettler-Toledo International Inc.
    "MU", # Micron Technology, Inc.
    "NCLH", # Norwegian Cruise Line Holdings Ltd.
    "NDAQ", # Nasdaq, Inc.
    "NDSN", # Nordson Corporation
    "NEE", # NextEra Energy, Inc.
    "NEM", # Newmont Corporation
    "NFLX", # Netflix, Inc.
    "NI", # NiSource Inc.
    "NKE", # NIKE, Inc.
    "NOC", # Northrop Grumman Corporation
    "NOW", # ServiceNow, Inc.
    "NRG", # NRG Energy, Inc.
    "NSC", # Norfolk Southern Corporation
    "NTAP", # NetApp, Inc.
    "NTRS", # Northern Trust Corporation
    "NUE", # Nucor Corporation
    "NVDA", # NVIDIA Corporation
    "NVR", # NVR, Inc.
    "NWS", # News Corporation
    "NWSA", # News Corporation
    "NXPI", # NXP Semiconductors N.V.
    "O", # Realty Income Corporation
    "ODFL", # Old Dominion Freight Line, Inc.
    "OKE", # ONEOK, Inc.
    "OMC", # Omnicom Group Inc.
    "ON", # ON Semiconductor Corporation
    "ORCL", # Oracle Corporation
    "ORLY", # O'Reilly Automotive, Inc.
    "OTIS", # Otis Worldwide Corporation
    "OXY", # Occidental Petroleum Corporation
    "PANW", # Palo Alto Networks, Inc.
    "PARA", # Paramount Global
    "PAYC", # Paycom Software, Inc.
    "PAYX", # Paychex, Inc.
    "PCAR", # PACCAR Inc
    "PCG", # PG&E Corporation
    "PEG", # Public Service Enterprise Group Incorporated
    "PEP", # PepsiCo, Inc.
    "PFE", # Pfizer Inc.
    "PFG", # Principal Financial Group, Inc.
    "PG", # The Procter & Gamble Company
    "PGR", # The Progressive Corporation
    "PH", # Parker-Hannifin Corporation
    "PHM", # PulteGroup, Inc.
    "PKG", # Packaging Corporation of America
    "PLD", # Prologis, Inc.
    "PLTR", # Palantir Technologies Inc.
    "PM", # Philip Morris International Inc.
    "PNC", # The PNC Financial Services Group, Inc.
    "PNR", # Pentair plc
    "PNW", # Pinnacle West Capital Corporation
    "PODD", # Insulet Corporation
    "POOL", # Pool Corporation
    "PPG", # PPG Industries, Inc.
    "PPL", # PPL Corporation
    "PRU", # Prudential Financial, Inc.
    "PSA", # Public Storage
    "PSX", # Phillips 66
    "PTC", # PTC Inc.
    "PWR", # Quanta Services, Inc.
    "PYPL", # PayPal Holdings, Inc.
    "QCOM", # QUALCOMM Incorporated
    "QRVO", # Qorvo, Inc.
    "RCL", # Royal Caribbean Cruises Ltd.
    "REG", # Regency Centers Corporation
    "REGN", # Regeneron Pharmaceuticals, Inc.
    "RF", # Regions Financial Corporation
    "RJF", # Raymond James Financial, Inc.
    "RL", # Ralph Lauren Corporation
    "RMD", # ResMed Inc.
    "ROK", # Rockwell Automation, Inc.
    "ROL", # Rollins, Inc.
    "ROP", # Roper Technologies, Inc.
    "ROST", # Ross Stores, Inc.
    "RSG", # Republic Services, Inc.
    "RTX", # RTX Corporation
    "RVTY", # Revvity, Inc.
    "SBAC", # SBA Communications Corporation
    "SBUX", # Starbucks Corporation
    "SCHW", # The Charles Schwab Corporation
    "SHW", # The Sherwin-Williams Company
    "SJM", # The J. M. Smucker Company
    "SLB", # Schlumberger Limited
    "SMCI", # Super Micro Computer, Inc.
    "SNA", # Snap-on Incorporated
    "SNPS", # Synopsys, Inc.
    "SO", # The Southern Company
    "SOLV", # Solventum Corporation
    "SPCE", # Virgin Galactic Holdings, Inc.
    "SPG", # Simon Property Group, Inc.
    "SPGI", # S&P Global Inc.
    "SRE", # Sempra
    "STE", # STERIS plc
    "STLD", # Steel Dynamics, Inc.
    "STT", # State Street Corporation
    "STX", # Seagate Technology Holdings plc
    "STZ", # Constellation Brands, Inc.
    "SW", # Smurfit Westrock Plc
    "SWK", # Stanley Black & Decker, Inc.
    "SWKS", # Skyworks Solutions, Inc.
    "SYF", # Synchrony Financial
    "SYK", # Stryker Corporation
    "SYY", # Sysco Corporation
    "T", # AT&T Inc.
    "TAP", # Molson Coors Beverage Company
    "TDG", # TransDigm Group Incorporated
    "TDY", # Teledyne Technologies Incorporated
    "TECH", # Bio-Techne Corporation
    "TEL", # TE Connectivity plc
    "TER", # Teradyne, Inc.
    "TFC", # Truist Financial Corporation
    "TFX", # Teleflex Incorporated
    "TGT", # Target Corporation
    "TJX", # The TJX Companies, Inc.
    "TMO", # Thermo Fisher Scientific Inc.
    "TMUS", # T-Mobile US, Inc.
    "TPR", # Tapestry, Inc.
    "TRGP", # Targa Resources Corp.
    "TRMB", # Trimble Inc.
    "TROW", # T. Rowe Price Group, Inc.
    "TRV", # The Travelers Companies, Inc.
    "TSCO", # Tractor Supply Company
    "TSLA", # Tesla, Inc.
    "TSN", # Tyson Foods, Inc.
    "TT", # Trane Technologies plc
    "TTWO", # Take-Two Interactive Software, Inc.
    "TXN", # Texas Instruments Incorporated
    "TXT", # Textron Inc.
    "TYL", # Tyler Technologies, Inc.
    "UAL", # United Airlines Holdings, Inc.
    "UBER", # Uber Technologies, Inc.
    "UDR", # UDR, Inc.
    "UHS", # Universal Health Services, Inc.
    "ULTA", # Ulta Beauty, Inc.
    "UNH", # UnitedHealth Group Incorporated
    "UNP", # Union Pacific Corporation
    "UPS", # United Parcel Service, Inc.
    "URI", # United Rentals, Inc.
    "USB", # U.S. Bancorp
    "V", # Visa Inc.
    "VICI", # VICI Properties Inc.
    "VLO", # Valero Energy Corporation
    "VLTO", # Veralto Corporation
    "VMC", # Vulcan Materials Company
    "VRSK", # Verisk Analytics, Inc.
    "VRSN", # VeriSign, Inc.
    "VRTX", # Vertex Pharmaceuticals Incorporated
    "VST", # Vistra Corp.
    "VTR", # Ventas, Inc.
    "VTRS", # Viatris Inc.
    "VZ", # Verizon Communications Inc.
    "WAB", # Westinghouse Air Brake Technologies Corporation
    "WAT", # Waters Corporation
    "WBA", # Walgreens Boots Alliance, Inc.
    "WBD", # Warner Bros. Discovery, Inc.
    "WDC", # Western Digital Corporation
    "WEC", # WEC Energy Group, Inc.
    "WELL", # Welltower Inc.
    "WFC", # Wells Fargo & Company
    "WM", # Waste Management, Inc.
    "WMB", # The Williams Companies, Inc.
    "WMT", # Walmart Inc.
    "WRB", # W. R. Berkley Corporation
    "WST", # West Pharmaceutical Services, Inc.
    "WTW", # Willis Towers Watson Public Limited Company
    "WY", # Weyerhaeuser Company
    "WYNN", # Wynn Resorts, Limited
    "XEL", # Xcel Energy Inc.
    "XOM", # Exxon Mobil Corporation
    "XYL", # Xylem Inc.
    "YUM", # Yum! Brands, Inc.
    "ZBH", # Zimmer Biomet Holdings, Inc.
    "ZBRA", # Zebra Technologies Corporation
    "ZTS", # Zoetis Inc.
]
