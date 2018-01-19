import threading
import control_dashboard
import spam


t0 = threading.Thread(target = control_dashboard.move_on_timestamps)
t1 = threading.Thread(target = spam.pulse_timestamps)

t0.start()
t1.start()

