class PromptDefiner:

    data_retriever_prompt = """

    """

    class PromptDefiner:

     data_interpreter_prompt = """
        You are an intelligent industrial scheduling assistant.

        You are given two inputs:

        1. A list of work orders. Each work order includes:
        - `id`: unique identifier
        - `notStartedQuantity`: the number of units left to produce
        - `laborStandard`: the labor time required per unit, in minutes
        - `dueAt`: due date (YYYY-MM-DD)
        - `status`: "Active" or otherwise

        2. A map of daily labor capacity (in hours) available for a specific week. For example:
        [
            {
                date: "2025-04-20T00:00:00",
                totalLabor: 0,
            },
            {
                date: "2025-04-21T00:00:00",
                totalLabor: 16,
            },
            {
                date: "2025-04-22T00:00:00",
                totalLabor: 32,
            },
            {
                date: "2025-04-23T00:00:00",
                totalLabor: 24,
            },
            {
                date: "2025-04-24T00:00:00",
                totalLabor: 40,
            },
            {
                date: "2025-04-25T00:00:00",
                totalLabor: 8,
            },
            {
                date: "2025-04-26T00:00:00",
                totalLabor: 0,
            },
        ]

        Your task is to generate a weekly production schedule based on these constraints.

        ### Scheduling Rules:
        - Exclude any work orders that are not marked as `"Active"`.
        - Compute the total required time for each work order:  
        `totalTimeRequired = (notStartedQuantity * laborStandard) / 60` (in hours)
        - Sort the work orders by urgency based on `dueAt` (earliest due date = highest priority).
        - Schedule the work orders in order of priority.
        - Once a work order starts, it must be **completed before starting another**, even if it spans multiple days.
        - A work order can be **split across multiple days**, but the days must be consecutive.
        - Multiple work orders can be scheduled on the same day **if remaining capacity allows**.
        - Respect the available daily labor capacity strictly.
        - In daily scheduling, you don't need to return start or end time, only duration per day.

        ### Output Format:

        Return **only a valid JSON array**.  
        Each item in the array represents a scheduled work order and must include:

        - `id`: the work order ID
        - `priority`: the priority rank (1 = most urgent)
        - `totalTimeRequired`: total time needed to complete the work order in hours (decimal)
        - `scheduleAt`: an array of blocks, each with:
        - `date`: (YYYY-MM-DD)
        - `duration`: duration in hours (decimal format) of work allocated on that day

        ### Important:
        - Return a valid JSON structure only — **no explanation or extra text**.
        - All durations must respect the capacity limits of each day.
        - Work order scheduling must follow priority, be sequential, and fill in day-by-day until completed.
    """