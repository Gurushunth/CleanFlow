import time
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from graph_builder import build_cleanflow_graph

def run_simulation():
    app = build_cleanflow_graph()
    
    # Tank total volume capacity: 2,500 m3
    TANK_VOLUME_CAPACITY_M3 = 2500.0
    
    # Initial Simulation State
    state = {
        "current_step": 0,
        "reservoir_level_pct": 18.0,  # Set at 18% to trigger real emergency drought override cycle
        "ro_plant_capacity_pct": 30.0,
        "grid_telemetry": None,
        "demand_forecast": None,
        "hydraulic_status": None,
        "proposed_ro_target_pct": 0.0,
        "emergency_override": False,
        "logs": [],
        "negotiation_cycle": 0,
        "operator_explanation": "",
        "scenario_overrides": None
    }

    print("==========================================================================")
    print("      CLEANFLOW: AUTONOMOUS DESALINATION & URBAN WATER GRID OPTIMIZER     ")
    print("           (100% Real Physical Fluid & Open-Meteo Multi-Agent Core)       ")
    print("==========================================================================")

    for step in range(5):
        state["current_step"] = step
        state["logs"] = []
        state["negotiation_cycle"] = 0
        
        # Execute multi-agent workflow
        output = app.invoke(state)
        
        target_ro = output["proposed_ro_target_pct"]
        demand = output["demand_forecast"].hourly_demand_m3
        hydr = output["hydraulic_status"]
        
        # Exact Mass-Balance Conservation Equation:
        # Water produced (m3/h) = (Target RO % / 100) * 500 m3/h max pump capacity
        # Net Flow (m3) = (Water Produced - Municipal Demand) * 1 hour step
        water_produced = (target_ro / 100.0) * 500.0
        net_flow_m3 = water_produced - demand
        
        # Level Delta % = (Net Flow m3 / Tank Capacity 2500 m3) * 100%
        level_delta_pct = (net_flow_m3 / TANK_VOLUME_CAPACITY_M3) * 100.0
        
        state["reservoir_level_pct"] = max(5.0, min(100.0, state["reservoir_level_pct"] + level_delta_pct))
        state["ro_plant_capacity_pct"] = target_ro
        
        print(f"\n--- [Cycle Step {step + 1}] ---")
        for log in output["logs"]:
            print(log)
            
        if hydr and hydr.zone_pressures:
            print("\n  📍 EPANET Multi-Zone Junction Pressures (Hazen-Williams Physics):")
            for zone, p_val in hydr.zone_pressures.items():
                print(f"     - {zone}: {p_val} PSI")
            print(f"     - Joukowsky Water Hammer Shockwave: +{hydr.transient_surge_psi} PSI")
            
        print(f"\n  💡 AI Operator Summary:\n     {output.get('operator_explanation', '')}")
        print(f"  --> Resulting Reservoir Storage: {state['reservoir_level_pct']:.2f}% ({state['reservoir_level_pct'] * 25.0:.1f} m³)")
        print(f"  --> Approved RO Production: {target_ro:.1f}% ({water_produced:.1f} m³/h)")
        print("-" * 74)
        time.sleep(0.8)

if __name__ == "__main__":
    run_simulation()
