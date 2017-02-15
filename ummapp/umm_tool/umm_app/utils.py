from .models import Process, SubProcess, ProgramType, ProgramTask, TaskData, SubProcessLevelUpdates, ProgramAdditionData
from django.core.exceptions import ObjectDoesNotExist


def delete_process(process_id):
    """

    Args:
        process_id: process ID

    """
    try:
        process = Process.objects.get(id=process_id)
    except ObjectDoesNotExist:
        return False

    sps = SubProcess.objects.filter(process=process)
    for sp in sps:
        program_types = ProgramType.objects.filter(subprocess=sp)
        for prog in program_types:
            tasks = ProgramTask.objects.filter(program_type=prog)
            for task in tasks:
                TaskData.objects.filter(program_task=task).delete()
                ProgramAdditionData.objects.filter(program_task=task).delete()
                task.delete()
            prog.delete()
        SubProcessLevelUpdates.objects.filter(subprocess=sp).delete()
        sp.delete()
    process.delete()
    return True


def delete_sub_process(subprocess_id):
    """

    Args:
        subprocess_id:
    """
    try:
        sp = SubProcess.objects.get(pk=subprocess_id)
    except ObjectDoesNotExist:
        return False
    program_types = ProgramType.objects.filter(subprocess=sp)
    for prog in program_types:
        tasks = ProgramTask.objects.filter(program_type=prog)
        for task in tasks:
            TaskData.objects.filter(program_task=task).delete()
            ProgramAdditionData.objects.filter(program_task=task).delete()
            task.delete()
        prog.delete()
    SubProcessLevelUpdates.objects.filter(subprocess=sp).delete()
    sp.delete()
    return True


def delete_program_types(program_ids):
    """

    Args:
        program_ids: Pass List of program IDs

    """
    program_types = ProgramType.objects.filter(pk__in=program_ids)
    for prog in program_types:
        tasks = ProgramTask.objects.filter(program_type=prog)
        for task in tasks:
            TaskData.objects.filter(program_task=task).delete()
            ProgramAdditionData.objects.filter(program_task=task).delete()
            task.delete()
        prog.delete()


def delete_program_tasks(task_ids):
    """

    Args:
        task_ids: Pass List of task IDs

    """
    tasks = ProgramTask.objects.filter(pk__in=task_ids)
    for task in tasks:
        TaskData.objects.filter(program_task=task).delete()
        ProgramAdditionData.objects.filter(program_task=task).delete()
        task.delete()
    return True


def delete_program_additional_data(additional_data_id):
    """

    Args:
        additional_data_id:

    """
    ProgramAdditionData.objects.get(pk=additional_data_id).delete()


def delete_task_data(task_data_id):
    """

    Args:
        task_data_id:

    """
    TaskData.objects.get(pk=task_data_id).delete()


def delete_subprocess_level_data(data_id):
    """

    Args:
        data_id:

    """
    SubProcessLevelUpdates.objects.get(pk=data_id).delete()
