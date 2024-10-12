from .models import SingleTask, PluralTask


class TaskManager:
    def __init__(self):
        self._list_tasks: list[SingleTask | PluralTask] = []

    def add_task(self, task: SingleTask | PluralTask) -> None:
        self._list_tasks.append(task)

    def get_task(self, uuid: str | None) -> SingleTask | PluralTask | None:
        task = list(filter(lambda t: t.uuid == uuid, self._list_tasks))
        return task[0] if task else None

    def handle_task(self, task_data: dict) -> None:
        task = self.get_task(task_data.get('taskUUID'))

        if isinstance(task, SingleTask):
            task.future.set_result(task_data)
        elif isinstance(task, PluralTask):
            task.results.append(task_data)

            if len(task.results) == task.amount_result:
                task.future.set_result(task.results)
