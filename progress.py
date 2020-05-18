import time 
import os 

def progress(i, lap_start, total, start_time, message="", frequency=0.5, precision=2, done=False):
        i += 1
        end_time = time.time()

        if end_time - lap_start < frequency and not done:
            return lap_start

        fraction = i / total
        percent = round(fraction * 100, precision)

        bar_len = 20
        done_len = int(bar_len * fraction)
        not_done_len = bar_len - done_len

        done = "#" * done_len
        not_done = " " * not_done_len

        remaining = total - i
        elapsed = end_time - start_time
        element_time = elapsed / i
        eta = round(element_time * remaining, precision)
        elapsed = round(elapsed, precision)

        try:
            os.system("cls")
        except:
            os.system("clear")
        template = f"Progress {i}/{total} |{done}{not_done}| {percent}% Elapsed: {elapsed}s ETA: {eta}s"
        print(template)
        print(message)

        return end_time