from typing import List, Optional
import os
from crewai import Task


def create_task(
    description: str,
    expected_output: str,
    agent,
    output_file: str,
    context: Optional[List] = None,
    async_execution: bool = False,
    human_input: bool = False
):
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        output_file=output_file,
        context=context if context else [],
        async_execution=async_execution,
        human_input=human_input
    )
