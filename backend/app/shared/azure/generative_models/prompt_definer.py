class PromptDefiner:

    data_retriever_prompt = """

    """

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
        {
        "2025-04-15": 8,
        "2025-04-16": 10,
        "2025-04-17": 12,
        "2025-04-18": 6,
        "2025-04-19": 8
        }

        Your task is to generate a weekly production schedule based on these constraints.

        ### Scheduling Rules:
        - Exclude any work orders that are not marked as `"Active"`.
        - Compute the total required time for each work order:  
        `totalTimeRequired = (notStartedQuantity × laborStandard) ÷ 60` (in hours)
        - Sort the work orders by urgency based on `dueAt` (earliest due date = highest priority).
        - Schedule the work orders in order of priority.
        - Once a work order starts, it must be **completed before starting another**, even if it spans multiple days.
        - A work order can be **split across multiple days**, but the segments must be consecutive.
        - Multiple work orders can be scheduled on the same day **if remaining capacity allows**.
        - Respect the available daily labor capacity strictly.
        - Daily scheduling starts at `"08:00"`. Continue scheduling work in sequence based on time available.

        ### Output Format:

        Return **only a valid JSON array**.  
        Each item in the array represents a scheduled work order and must include:

        - `id`: the work order ID
        - `priority`: the priority rank (1 = most urgent)
        - `segments`: an array of scheduled time blocks, each with:
        - `date`: (YYYY-MM-DD)
        - `start`: start time (HH:MM)
        - `end`: end time (HH:MM)
        - `duration`: duration in hours (decimal format)

        ### Important:
        - Return a valid JSON structure only — **do not include any explanation or extra text**.
        - All time calculations must strictly follow the available capacity per day.
        - All time segments must be placed sequentially and respect the constraints.

    """



    [
              {
                week: "2025-04-12",
                user: "abdelaziz.kamomegna@entrust.com",
                line: "Sigma",
                shiftId: "SHIFT123",
                monday: {
                  start: "06:00",
                  end: "14:30",
                  exception: "Half-day due to training",
                },
                tuesday: {
                  start: "08:00",
                  end: "16:30",
                  exception: "Late start due to equipment maintenance",
                },
                wednesday: {
                  start: "07:00",
                  end: "12:30",
                  exception: "Emergency leave",
                },
                thursday: { start: "06:00", end: "15:00", exception: "" },
                friday: {
                  start: "06:00",
                  end: "13:00",
                  exception: "System outage",
                },
                saturday: {
                  start: "07:00",
                  end: "11:30",
                  exception: "Overtime approved",
                },
                sunday: { start: null, end: null, exception: "Not working" },
              },
              {
                week: "2025-04-19",
                user: "abdelaziz.kamomegna@entrust.com",
                line: "Sigma",
                shiftId: null,
                monday: { start: "06:00", end: "14:30", exception: "" },
                tuesday: { start: null, end: null, exception: "Medical leave" },
                wednesday: {
                  start: "08:00",
                  end: "16:00",
                  exception: "Shift swapped",
                },
                thursday: { start: "06:00", end: "14:30", exception: "" },
                friday: {
                  start: "06:00",
                  end: "12:00",
                  exception: "Early finish approved",
                },
                saturday: { start: null, end: null, exception: "Not working" },
                sunday: { start: null, end: null, exception: "Not working" },
              },
            ]