import threading
import control_dashboard
import spam

bus = control_dashboard.can_init('can0')

light_timestamps = open('beat_times.csv', 'r').readlines()
light_timestamps = [float(l.strip()) for l in light_timestamps]
rev_timestamps, mph_timestamps = control_dashboard.get_timestamps() 

dash_thread = threading.Thread(target = control_dashboard.move_on_timestamps, args=(bus,rev_timestamps, mph_timestamps))
lights_thread = threading.Thread(target = spam.pulse_timestamps, args=(bus,light_timestamps))

dash_thread.start()
lights_thread.start()

