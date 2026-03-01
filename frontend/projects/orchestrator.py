from .critic import run_critic
from .monitor import check_project_overdue


def run_post_task_agents(project):
    """
    Central coordination point for all post-task agents.
    """

    # 1. Health evaluation
    run_critic(project)

    # 2. Deadline monitoring
    check_project_overdue(project)