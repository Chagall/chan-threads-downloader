def print_execution_time(start_time, end_time):
    total_time = end_time - start_time
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    seconds = int(total_time % 60)
    milliseconds = int((total_time - int(total_time)) * 1000)

    if hours > 0:
        print(
            f"Tempo de download: {hours:02d} horas {minutes:02d} minutos {seconds:02d} segundos e {milliseconds:03d} milissegundos"
        )
    elif minutes > 0:
        print(f"Tempo de download: {minutes:02d} minutos {seconds:02d} segundos e {milliseconds:03d} milissegundos")
    elif seconds > 0:
        print(f"Tempo de download: {seconds:02d} segundos e {milliseconds:03d} milissegundos")
