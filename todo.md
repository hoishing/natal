# todo

- speed test: swiss vs Moshier
- calc_ut() default flag: swe.FLG_SWIEPH | swe.FLG_SPEED
    - need [0] deg and [3] speed only
- swe.house_name, .get_planet_name(int)
- swe.houses -> cusps -> hse degree % 30
    - hse_sys: binary char
    - return: 12 tuple of float, 8 tuple of points (0=ASC, 1=MC)
- flag
    - geocentric: FLG_TRUEPOS
    - kerykeion default: swe.FLG_SWIEPH + swe.FLG_SPEED
    - use |= instead of +=

Date (d.m.y) ? (type . to exit) : 20.4.1976
date: 20.04.1976 at 0:00 Universal time
julian day: 2442888

| planet    | longitude   | latitude   | distance   | speed long. |
| --------- | ----------- | ---------- | ---------- | ----------- |
| Sun       | 30.0386877  | 0.0000402  | 1.0047498  | 0.9760844   |
| Moon      | 284.2918454 | 4.6577161  | 0.0025487  | 13.3392903  |
| Mercury   | 47.8531924  | 2.0604912  | 1.0493889  | 1.5974471   |
| Venus     | 14.3195395  | -1.4957519 | 1.6405050  | 1.2311057   |
| Mars      | 105.6942936 | 1.9256851  | 1.5945183  | 0.5200818   |
| Jupiter   | 35.7834134  | -0.9708944 | 5.9691697  | 0.2389947   |
| Saturn    | 116.5153483 | 0.4051510  | 9.0900950  | 0.0415307   |
| Uranus    | 215.3414022 | 0.5126246  | 17.5186644 | -0.0423250  |
| Neptune   | 253.6482369 | 1.5601017  | 29.5599025 | -0.0175143  |
| Pluto     | 189.7997951 | 17.4510074 | 29.7293587 | -0.0257443  |
| mean Node | 223.4420421 | 0.0000000  | 0.0025696  | -0.0529421  |
| Chiron    | 27.8028639  | 0.1623438  | 19.2463453 | 0.0605809   |