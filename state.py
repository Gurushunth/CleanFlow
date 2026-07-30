from typing import TypedDict, List, Dict, Optional, Any
from pydantic import BaseModel, Field

class GridStatus(BaseModel):
    spot_price_per_kwh: float  # in INR / USD
    renewable_percentage: float  # 0 to 100%
    grid_stress_level: str  # LOW, MEDIUM, HIGH

class WaterDemandForecast(BaseModel):
    hourly_demand_m3: float
    temperature_celsius: float
    is_peak_hour: bool

class HydraulicSafetyStatus(BaseModel):
    max_node_pressure_psi: float
    min_node_pressure_psi: float
    cavitation_risk: bool
    is_safe: bool
    critical_node_id: Optional[str] = None
    zone_pressures: Dict[str, float] = Field(default_factory=dict)
    transient_surge_psi: float = 0.0

class DesalinationState(TypedDict):
    current_step: int
    reservoir_level_pct: float
    ro_plant_capacity_pct: float
    grid_telemetry: Optional[GridStatus]
    demand_forecast: Optional[WaterDemandForecast]
    hydraulic_status: Optional[HydraulicSafetyStatus]
    proposed_ro_target_pct: float
    emergency_override: bool
    logs: List[str]
    negotiation_cycle: int
    operator_explanation: str
    scenario_overrides: Optional[Dict[str, Any]]
