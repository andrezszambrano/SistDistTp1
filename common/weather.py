

class Weather:
    def __init__(self, date, prectot, qv2m, rh2m, ps, t2m_range, ts, t2mdew, t2mwet, t2m_max, t2m_min, t2m, ws50m_range,
                 ws10m_range, ws50m_min, ws10m_min, ws50m_max, ws10m_max, ws50m, ws10m):
        self.date = date
        self.prectot = prectot
        self.qv2m = qv2m
        self.rh2m = rh2m
        self.ps = ps
        self.t2m_range = t2m_range
        self.ts = ts
        self.t2mdew = t2mdew
        self.t2mwet = t2mwet
        self.t2m_max = t2m_max
        self.t2m_min = t2m_min
        self.t2m = t2m
        self.ws50m_range = ws50m_range
        self.ws10m_range = ws10m_range
        self.ws50m_min = ws50m_min
        self.ws10m_min = ws10m_min
        self.ws50m_max = ws50m_max
        self.ws10m_max = ws10m_max
        self.ws50m = ws50m
        self.ws10m = ws10m

    def info(self):
        return f"WEATHER: {self.date}, {self.prectot}"
