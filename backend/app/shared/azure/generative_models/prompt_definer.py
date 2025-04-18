class PromptDefiner:

    data_interpreter_prompt = """
        You are a smart industrial scheduling assistant.

        You are given two inputs:

        1. A list of work orders. Each work order includes:
        - `id`: unique identifier
        - `notStartedQuantity`: number of units left to produce
        - `laborStandard`: time required per unit (in minutes)
        - `dueAt`: due date (YYYY-MM-DD)
        - `status`: "Active" or otherwise

        2. A list of available labor hours per day for a given week:
        Example format:
        [
        { "date": "2025-04-21T00:00:00", "totalLabor": 16 },
        { "date": "2025-04-22T00:00:00", "totalLabor": 8 },
        ...
        ]

        ---

        ### Your Task:

        Create a prioritized and time-efficient production schedule, following the rules below.

        #### Scheduling Rules:
        - Exclude work orders that are **not marked as "Active"**
        - Calculate `totalTimeRequired` = (`notStartedQuantity` × `laborStandard`) / 60 (in hours)
        - Sort all active work orders by `dueAt` (earliest first = highest priority)
        - Assign a `priority` rank to each (1 = most urgent)
        - Distribute the total time of each work order across available daily capacity (`totalLabor`)
        - Fill **each day’s capacity fully before moving to the next**
        - A work order can **span multiple consecutive days**
        - Once started, a work order must be **completed before starting another**
        - Multiple work orders can share a day **only if capacity remains after previous is completed**
        - Do **not skip available capacity on earlier days** even if a due date is later
        - All durations must strictly respect daily labor limits

        ---

        ### Output Format:

        Return a **valid JSON array** only.  
        Each element must represent a scheduled work order in the following structure:

        ```json
        [
            {
                "id": "WO-001",
                "priority": 1,
                "totalTimeRequired": 18,
                "scheduleAt": [
                { "date": "2025-04-21", "duration": 8 },
                { "date": "2025-04-22", "duration": 8 },
                { "date": "2025-04-23", "duration": 2 }
                ]
            },
        ...
        ]

        ### Important:

        - Return only the JSON array, no explanation, titles, or comments
        - Respect every constraint carefully
        - Round durations to 1 decimal if needed (e.g., 7.5 hours)
        - Ensure the output is always valid JSON and can be parsed directly
    """