#!/usr/bin/env python3

from mailcleaner.db import base
from mailcleaner.db.helpers import MCGaugeCounterDeriveEnum, MCAverageMinMaxEnum, MCLineAreaStackEnum
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class RRDStatsElement(base, BaseModel):
    """
    rrd_stats_element table
    """
    __tablename__ = 'rrd_stats_element'

    id = Column(INTEGER(11), nullable=False, primary_key=True)
    stats_id = Column(INTEGER(11), nullable=False)
    name = Column(String(255), nullable=True)
    type = Column(Enum(MCGaugeCounterDeriveEnum), nullable=True, default=MCGaugeCounterDeriveEnum.COUNTER.value)
    function = Column(Enum(MCAverageMinMaxEnum), nullable=True, default=MCAverageMinMaxEnum.AVERAGE.value)
    oid = Column(String(255), nullable=True)
    min = Column(String(255), nullable=True, default="U")
    max = Column(String(255), nullable=True, default="U")
    draw_name = Column(String(255), nullable=True)
    draw_order = Column(INTEGER(11), nullable=False, default=1)
    draw_style = Column(Enum(MCLineAreaStackEnum), nullable=True, default=MCLineAreaStackEnum.line.value)
    draw_factor = Column(String(255), nullable=True)
    draw_format = Column(String(255), nullable=True, default="8.0lf")
    draw_unit = Column(String(255), nullable=True)
