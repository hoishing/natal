from dataclasses import dataclass


@dataclass
class NatalData:
    """Data object for a natal chart.

    Attributes:
        name: The name of the person the chart is for.
        yr: The year of birth.
        mo: The month of birth.
        day: The day of birth.
        hr: The hour of birth.
        min: The minute of birth.
        city: The city of birth.

    Example:
        >>> Natal("Alice", 1990, 1, 1, 12, 0, "New York")
        Natal(name='Alice', yr=1990, mo=1, day=1, hr=12, min=0, city='New York

    """

    name: str
    yr: int
    mo: int
    day: int
    hr: int
    min: int
    city: str
