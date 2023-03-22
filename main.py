import multiprocessing
import dock_overlay

if __name__ == '__main__':
    dock_overlay_process = multiprocessing.Process(target=dock_overlay.run_overlay)
    dock_overlay_process.start()
    dock_overlay_process.join() 