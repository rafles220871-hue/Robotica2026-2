import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/robotics/Prácticas/Robotica2026-2/proyecto_ws/install/robot_description'
