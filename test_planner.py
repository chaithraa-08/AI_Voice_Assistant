from agents.planner import PlannerAgent

planner = PlannerAgent()

plan = planner.create_plan(
    "Open Chrome and search for Python tutorials"
)

print("\nParsed Plan:\n")
print(plan)